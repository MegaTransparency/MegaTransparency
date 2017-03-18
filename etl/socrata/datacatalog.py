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
    cpus = multiprocessing.cpu_count() * 20
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

def get_catalog_for_region(region, hidden=False):
    if hidden:
        hidden = '&domains=moto.data.socrata.com,odn.data.socrata.com,opendata.socrata.com'
    else:
        hidden = ''
    results = []
    query_results = requests.get('http://api.%s.socrata.com/api/catalog/v1?only=datasets%s&limit=10000' % (region, hidden), timeout=10)
    query_results = query_results.json()
    results.extend(query_results['results'])
    datasets_count = query_results['resultSetSize']
    loops = int(math.ceil(float(datasets_count) / 10000))
    
    pool = multiprocessing.Pool(processes=cpus)
    for result in pool.map(get_dataset_list, [(region, i, hidden) for i in range(1, loops)]):
        results.extend(result)
    pool.close()
    for i, row in enumerate(results):
        results[i] = flatten_dict(row)
        results[i]['api_url'] = results[i]['permalink'].replace('/d/', '/resource/') + '.json'
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
        with open(os.path.join(dir_of_script, 'datacatalog.json'), 'r') as f:
            old_rows = dict([(json.loads(row)['resource_id'], json.loads(row)) for row in f.readlines()])
        datasets_to_ignore = ['avj9-39zb'] # these sets are replaced everytime I check so pointless to look at them
        changed_results = [row for row in fresh_catalog if row['resource_updatedAt'] != old_rows.get(row['resource_id'], {}).get('resource_updatedAt', '') and row['resource_id'] not in datasets_to_ignore]
    else:
        changed_results = fresh_catalog
    if changed_results:
        pool = multiprocessing.Pool(processes=cpus)
        results = pool.map(add_count, changed_results)
        pool.close()
        if old_rows:
            for row in results:
                old_rows[row['resource_id']] = row
            results = old_rows.values()
        with open(catalog_file, 'w') as f:
            f.write('\n'.join([json.dumps(row) for row in results]))
        cmd = 'bq load --replace --max_bad_records=10000 --source_format=NEWLINE_DELIMITED_JSON %s %s &>/dev/null &' % (bigquery_table, catalog_file)
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