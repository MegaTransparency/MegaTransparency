import collections
import requests
import json
import os
import multiprocessing
import math
import traceback
import sys

# This script makes and updates a public BigQuery table of every dataset hosted on Socrata
# documentation of the socrata discovery API is at http://docs.socratadiscovery.apiary.io/#
dir_of_script = os.path.dirname(os.path.realpath(__file__))
catalog_file = os.path.join(dir_of_script, 'datacatalog.json')
with open(os.path.join(dir_of_script, 'config.json'), 'r') as f:
    config = json.loads(f.read())

app_token = config.get('socrata_api_token', '')
bigquery_table = config.get('bigquery_table')
try:
    cpus = multiprocessing.cpu_count()
except NotImplementedError:
    cpus = 2   # arbitrary default

# flatten_dict comes from http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
def flatten_dict(dd, separator='_', prefix=''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

def get_dataset_list(info):
    region, i, hidden = info
    return requests.get('http://api.%s.socrata.com/api/catalog/v1?only=datasets%s&limit=10000&offset=%s' % (region, hidden, str(10000*i)), timeout=10).json()['results']

def get_2_point_1_id(row):
    row = flatten_dict(row)
    try:
        s = requests.Session()
        a = requests.adapters.HTTPAdapter(max_retries=1)
        s.mount('http://', a)
        url = 'https://%s/api/migrations/%s.json' % (row['metadata_domain'], row['resource_id'])
        return (row['metadata_domain'] + '_' + row['resource_id'], s.get(url, timeout=2, verify=False).json().get('nbeId', ''))
    except:
        return (row['metadata_domain'] + '_' + row['resource_id'], 'doesnt_exist')

def get_catalog_for_region(region, hidden=False):
    if hidden:
        hidden = '&domains=moto.data.socrata.com,odn.data.socrata.com,opendata.socrata.com'
    else:
        hidden = ''
    results = []
    url = 'http://api.%s.socrata.com/api/catalog/v1?only=datasets%s&limit=10000' % (region, hidden)
    print 'URL', url
    query_results = requests.get(url, timeout=10)
    query_results = query_results.json()
    results.extend(query_results['results'])
    datasets_count = query_results['resultSetSize']
    loops = int(math.ceil(float(datasets_count) / 10000))
    try:
        pool = multiprocessing.Pool(processes=cpus)
        for result in pool.map(get_dataset_list, [(region, i, hidden) for i in range(1, loops)]):
            results.extend(result)
        pool.close()
    except KeyboardInterrupt:
        os.system("kill -9 $(ps aux | grep '[p]ython FreeOpenData/etl/socrata/datacatalog.py' | awk '{print $2}')")
        raise KeyboardInterruptError()
    try:
        pool = multiprocessing.Pool(processes=cpus)
        two_point_1_ids = dict(pool.map(get_2_point_1_id, results))
        pool.close()
    except KeyboardInterrupt:
        os.system("kill -9 $(ps aux | grep '[p]ython FreeOpenData/etl/socrata/datacatalog.py' | awk '{print $2}')")
        raise KeyboardInterruptError()
    rows_to_remove = []
    for i, row in enumerate(results):
        results[i] = flatten_dict(row)
        results[i]['api_url'] = results[i]['permalink'].replace('/d/', '/resource/') + '.json'
        row = results[i]
        key = row['metadata_domain'] + '_' + row['resource_id']
        results[i]['id_for_2_point_1_api'] = two_point_1_ids[key]
        if two_point_1_ids[key] == 'doesnt_exist':
            rows_to_remove.append(i)
    for i, row_i in enumerate(rows_to_remove):
        del results[row_i-i]
    return results

def generate_catalog():
    results = []
    for region in ['us', 'eu']: 
        results.extend(get_catalog_for_region(region))
    results.extend(get_catalog_for_region('us', True))
    return results
 
    
def add_count(result):
    try:
        count_url = '%s?$select=count(*)&$$app_token=%s' % (result['api_url'], app_token)
        count_data = None
        count_data = requests.get(count_url, verify=False, timeout=10).json()
        result['number_of_rows'] = int(count_data[0][count_data[0].keys()[0]]) # sometimes key is count_1 instead of count
    except:
        pass
    return result

def update_catalog():
    fresh_catalog = generate_catalog()
    old_rows = []
    if os.path.exists(catalog_file):
        with open(catalog_file, 'r') as f:
            old_rows = dict([(json.loads(row)['resource_id'], json.loads(row)) for row in f.readlines()])
        datasets_to_ignore = ['avj9-39zb'] # these sets are replaced everytime I check so pointless to look at them
        changed_results = [row for row in fresh_catalog if row['resource_updatedAt'] != old_rows.get(row['resource_id'], {}).get('resource_updatedAt', '') and row['resource_id'] not in datasets_to_ignore]
    else:
        changed_results = fresh_catalog
    if changed_results:
        try:
            pool = multiprocessing.Pool(processes=cpus)
            results = pool.map(add_count, changed_results)
            pool.close()
        except KeyboardInterrupt:
            os.system("kill -9 $(ps aux | grep '[p]ython FreeOpenData/etl/socrata/datacatalog.py' | awk '{print $2}')")
            raise KeyboardInterruptError()
        fresh_rows = dict([(row['resource_id'], row) for row in fresh_catalog])
        for row in results:
            fresh_rows[row['resource_id']] = row
        results = fresh_rows.values()
        with open(catalog_file, 'w') as f:
            f.write('\n'.join([json.dumps(row) for row in results]))
        cmd = 'bq load --autodetect --replace --max_bad_records=10000 --source_format=NEWLINE_DELIMITED_JSON %s %s &>/dev/null &' % (bigquery_table, catalog_file)
        print cmd
        os.system(cmd)

while True:
    try:
        update_catalog()
    except OSError, MemoryError:
        os.execv(sys.executable, ['python', __file__])
    except KeyboardInterrupt:
        os.system("kill -9 $(ps aux | grep '[p]ython etl/socrata/datacatalog.py' | awk '{print $2}')")
        sys.exit()
    except Exception, err:
        traceback.print_exc()