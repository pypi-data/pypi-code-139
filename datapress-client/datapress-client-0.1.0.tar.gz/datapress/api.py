import logging
import os
import requests
import dotenv
import hashlib
import pandas as pd

logger = logging.getLogger(__name__)

# Fetch the environment variables
dotenv.load_dotenv()

# Set the logging level by environment variable
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def _get_connection_var(env_key, default=None):
    """
    Private method to fetch a connection variable from the environment,
    or use a default value if provided.
    """
    if os.environ.get(env_key):
        if default is not None:
            logger.warning(
                '%s environment variable is set; ignoring default value', env_key)
        return os.environ.get(env_key)
    if default is None:
        raise Exception('%s is not set in the environment' % env_key)
    return default


def _get_connection(site_url=None, dataset=None, script_id=None, api_key=None):
    """
    Get all the DataPress connection variables
    """
    return {
        'site_url': _get_connection_var('DATAPRESS_URL', site_url),
        'dataset': _get_connection_var('DATAPRESS_DATASET', dataset),
        'script_id': _get_connection_var('DATAPRESS_SCRIPT', script_id),
        'api_key': _get_connection_var('DATAPRESS_API_KEY', api_key),
    }


def get_files(site_url=None, dataset=None, script_id=None):
    """
    Fetch all the XLSX/CSV resource files associated with this script, as configured on the dataset.
    """
    conn = _get_connection(site_url, dataset, script_id)
    dataset_url = conn['site_url'] + '/api/dataset/' + conn['dataset']
    dataset = requests.get(dataset_url).json()
    script = dataset['scripts'][conn['script_id']]
    resource_ids = script['resources']
    resource_urls = list(
        map(
            lambda id: dataset['resources'][id]['url'], resource_ids
        )
    )
    files = {}
    for (i, url) in enumerate(resource_urls):
        # Get the filename (decoding the URL)
        encoded_filename = url.split('/')[-1]
        filename = requests.utils.unquote(encoded_filename).lower()
        logger.info('Downloading file %d of %d: %s', i + 1,
                    len(resource_urls), filename)
        # If it's an .xlsx file, open a pandas dataframe
        if filename.endswith('.xlsx'):
            files[filename] = pd.read_excel(url + '?redirect=true')
        # If it's a .csv file, similar
        elif filename.endswith('.csv'):
            files[filename] = pd.read_csv(url)
        else:
            logger.info('Skipping unrecognised file type: %s', filename)
            # files[filename] = requests.get(url).content
    return files


def _commit_csv(conn, csv_data, name, type):
    """Private method: Upload a table or chart via a pre-signed link"""
    if (type != 'chart' and type != 'table'):
        # Invalid value
        raise ValueError('Invalid type: %s' % type)

    # Request a presigned upload from the website, at
    # /api/dataset/:id/presign/script/:script_id/table/:table_id
    presign_url = '/'.join([
        conn['site_url'],
        'api',
        'dataset',
        conn['dataset'],
        'presign',
        'script',
        conn['script_id'],
        type,
        name,
    ])
    presign = requests.post(presign_url, headers={
        'Authorization': conn['api_key']}).json()

    # Response format:
    # {
    #   "url": "https://ams3.digitaloceanspaces.com/datapress-files",
    #   "fields": {
    #     "bucket": "datapress-files",
    #     "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
    #     "X-Amz-Credential": "[credential]",
    #     "X-Amz-Date": "[date]",
    #     "key": "[path to upload]",
    #     "Policy": "[hashed policy]",
    #     "X-Amz-Signature": "[my signature]"
    #   }
    # }

    # Upload the file to the one-time URL
    logger.debug('POST %s', presign['url'])
    requests.post(presign['url'], data=presign['fields'], files={
        'file': csv_data
    })
    return presign['fields']['key']


def commit_table(df, name, site_url=None, dataset=None, script_id=None):
    """Upload a table to DataPress.
    Provide a kebab-case-name for the table, and a pandas dataframe."""
    logger.info('Uploading table: "%s"', name)
    conn = _get_connection(site_url, dataset, script_id)

    # Fetch the dataset metadata
    dataset_url = conn['site_url'] + '/api/dataset/' + conn['dataset']
    dataset = requests.get(dataset_url).json()
    tables = dataset['scripts'][conn['script_id']]['tables']

    csv_data = df.to_csv(index=False).encode('utf-8')

    # Deduplicate
    if name in tables:
        old_hash = tables[name]['csvHash']
        new_hash = hashlib.md5(csv_data).hexdigest()
        if old_hash == new_hash:
            logger.info('Skipping table: "%s" (CSV is unchanged)', name)
            return

    csv_key = _commit_csv(conn, csv_data, name, 'table')

    # Fetch the dataset metadata
    dataset = requests.get(dataset_url).json()
    path = "/scripts/" + conn['script_id'] + "/tables/" + name
    if name not in tables:
        patch = [
            {  # Test that the table does not exist
                'op': 'test',
                'path': path,
                'value': None,
            },
            {   # Add the table
                "op": "add",
                "path": path,
                "value": {'csv': csv_key}
            }
        ]
    else:
        patch = [
            {   # Update the script's table key on DataPress
                "op": "replace",
                "path": path + '/csv',
                "value": csv_key
            }
        ]
    requests.patch(dataset_url, headers={
        'Authorization': conn['api_key']}, json=patch)


def commit_chart(df, name, site_url=None, dataset=None, script_id=None):
    """Upload a table to DataPress.

    Provide a kebab-case-name for the table, and a pandas dataframe.
    The output CSV must be under 100kb."""
    logger.info('Uploading chart: "%s"', name)
    conn = _get_connection(site_url, dataset, script_id)

    # Fetch the dataset metadata
    dataset_url = conn['site_url'] + '/api/dataset/' + conn['dataset']
    dataset = requests.get(dataset_url).json()
    charts = dataset['scripts'][conn['script_id']]['charts']

    csv_data = df.to_csv(index=False).encode('utf-8')
    if (len(csv_data) > 1024 * 100):
        raise Exception('Chart CSV data must be under 100kb')

    # Deduplicate
    if name in charts:
        old_hash = charts[name]['csvHash']
        new_hash = hashlib.md5(csv_data).hexdigest()
        if old_hash == new_hash:
            logger.info('Skipping chart: "%s" (CSV is unchanged)', name)
            return

    csv_key = _commit_csv(conn, csv_data, name, 'chart')

    path = "/scripts/" + conn['script_id'] + "/charts/" + name
    if name not in charts:
        patch = [
            {  # Test that the table does not exist
                'op': 'test',
                'path': path,
                'value': None,
            },
            {   # Add the table
                "op": "add",
                "path": path,
                "value": {'csv': csv_key}
            }
        ]
    else:
        # Update the script's table key on DataPress
        patch = [
            {
                "op": "replace",
                "path": path + '/csv',
                "value": csv_key
            }
        ]
    requests.patch(dataset_url, headers={
        'Authorization': conn['api_key']}, json=patch)
