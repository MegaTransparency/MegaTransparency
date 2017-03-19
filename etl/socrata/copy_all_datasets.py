import collections
import requests
import json
import os
import multiprocessing
import math
import traceback
import sys

# This script copies all known Socrata datasets to BigQuery and appends new rows
# It doesn't deal with deletes or updates yet because of the cost of doing so in the 
# BigQuery API https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language
# Plan is to make a dataset of updates

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

def copy_dataset(dataset):
    domain = dataset['domain']
    did = dataset['id']
    try:
        new_did = requests.get('https://%s/api/migrations/%s.json' % (domain, did)).json().get('nbeId')
        if not new_did:
            new_did = did
        url = 'https://%s/resource/%s.json?$select=:updated_at&$order=:updated_at DESC&$limit=1&$$app_token=%s' % (domain, new_did, app_token)
        last_update = str(requests.get(url).json()[0][':updated_at'])
        columns = ','.join([row['fieldName'] for row in requests.get('https://%s/views/%s.json' % (domain, did)).json()['columns']])
        path = '/home/main/gdriveforfod/public/socrata_data/%s_%s_%s.csv' % (domain.replace('.', '_'), did.replace('-', '_'), last_update)
        os.system('wget "https://%s/resource/%s.csv?\$select=:id as socrata_id,:updated_at as socrata_updated_at,:created_at as socrata_created_at,%s&\$limit=90000000&\$\$app_token=%s&\$where=:updated_at <= %s%s%s" -O %s' % (domain, new_did, columns, app_token, '' if last_update.isdigit() else "'", last_update, '' if last_update.isdigit() else "'", path))
        if os.stat(path).st_size==0:
            os.system('rm %s' % (path))
            return
        cmd = 'bq load --autodetect --max_bad_records=10000000 --skip_leading_rows=1 --source_format=CSV copy_of_socrata_data.%s_%s /home/main/gdriveforfod/public/socrata_data/%s_%s_%s.csv' % (domain.replace('.', '_'), did.replace('-', '_'), domain.replace('.', '_'), did.replace('-', '_'), last_update)
        print cmd
        os.system(cmd)
    except KeyboardInterrupt:
        os.system("kill -9 $(ps aux | grep '[p]ython etl/socrata/copy_all_datasets.py' | awk '{print $2}')")
        raise KeyboardInterruptError()
    except Exception, err:
        
        traceback.print_exc()
        return
    return (domain+'_'+did, last_update)

def copy_all_the_data():
    # load the data catalog
    with open(catalog_file, 'r') as f:
        old_rows = [json.loads(row) for row in f.readlines()]
    datasets_to_copy = [{'domain': row['metadata_domain'], 'id': row['resource_id']} for row in old_rows]
    print datasets_to_copy
    last_update_times = {}
    pool = multiprocessing.Pool(processes=cpus)
    last_update_times = dict([row for row in pool.map(copy_dataset, datasets_to_copy) if row])
    pool.close()
    with open(os.path.join(dir_of_script, 'last_update_times.json'), 'w') as f:
        f.write(json.dumps(last_update_times))

while True:
    try:
        copy_all_the_data()
    except OSError, MemoryError:
        os.execv(sys.executable, ['python', __file__])
    except KeyboardInterrupt:
        os.system("kill -9 $(ps aux | grep '[p]ython etl/socrata/copy_all_datasets.py' | awk '{print $2}')")
        sys.exit()
    except Exception, err:
        traceback.print_exc()
    break