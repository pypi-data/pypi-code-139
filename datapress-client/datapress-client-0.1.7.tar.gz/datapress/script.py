import inspect
import logging
import os
import requests
import dotenv
import hashlib
import pandas as pd
import io
import json
import sys

logger = logging.getLogger(__name__)

# Set the logging level by environment variable
logging_level = os.environ.get('LOGLEVEL', 'INFO') or 'INFO'
logging.basicConfig(level=logging_level,
                    format='%(levelname)s %(message)s')
# Send INFO logs to stdout, not stderr
logging.getLogger().handlers[0].stream = sys.stdout
logger.info('LOGLEVEL=' + logging_level)

# Cached instance of ScriptClient for this script run
_client = None


def get_client():
    global _client
    if (_client is None):
        _client = ScriptClient()
    return _client


# ----------------------
# Convenience functions wrapping the client object
# ----------------------

def load_dataframes():
    return get_client().load_dataframes()


def commit_table(name, df):
    get_client().commit_table(name, df)


def commit_chart(name, df):
    get_client().commit_chart(name, df)


# ----------------------
# Used by .ipynb scripts to chat to the DataPress API
# ----------------------
class ScriptClient:
    # ----------------------
    # Internal static methods
    # ----------------------
    @staticmethod
    def _get_script_path():
        """
        Get the path to the script that is running this code.
        If this module is being imported by an iPython notebook running in vscode,
        get the path to that notebook instead.
        """
        # Search through the scope of globals() throughout the calling stack
        for frame in inspect.stack():
            if '__vsc_ipynb_file__' in frame.frame.f_globals:
                return frame.frame.f_globals['__vsc_ipynb_file__']
        # Huh, not in VSCode. Try to get the path from the stack trace
        # Walk through the stack from the bottom up
        for frame in reversed(inspect.stack()):
            # Get the filename from the frame
            filename = frame.filename
            # If it's not this file, then it's the script that called this file
            if filename != __file__ and filename.endswith('.py'):
                return os.path.abspath(filename)

    @staticmethod
    def _load_all_dotenvs():
        path = ScriptClient._get_script_path()
        # (1) load .env, if it exists
        if (dotenv.find_dotenv()):
            logger.info('[env vars] Loading: ' + dotenv.find_dotenv())
            dotenv.load_dotenv()
        else:
            expected_file = os.path.join(os.path.dirname(path), '.env')
            logger.info(
                '[env vars] Skipping (file not found): ' + expected_file)
        # (2) load [scriptname].env, if it exists
        # eg. if you're in "accidents.ipynb", look for "accidents.env"
        filename = os.path.splitext(path)[0] + '.env'
        filepath = os.path.join(os.path.dirname(path), filename)
        if (os.path.exists(filepath)):
            logger.info('[env vars] Loading: ' + filepath)
            dotenv.load_dotenv(filepath)
        else:
            logger.info('[env vars] Skipping (file not found): ' + filename)

    def __init__(self):
        """
        Create an API connection to DataPress.
        Automatically loads .env and [notebookname].env files.

        Uses environment variables:
        * DATAPRESS_URL
        * DATAPRESS_API_KEY
        * DATAPRESS_SCRIPT
        * DATAPRESS_DATASET

        Scripts deployed to DataPress should rely entirely on environment variables.
        """
        # Fetch the env vars
        ScriptClient._load_all_dotenvs()
        missing = []
        if os.environ.get('DATAPRESS_URL') is None:
            missing.append('DATAPRESS_URL')
        if os.environ.get('DATAPRESS_API_KEY') is None:
            missing.append('DATAPRESS_API_KEY')
        if os.environ.get('DATAPRESS_DATASET') is None:
            missing.append('DATAPRESS_DATASET')
        if os.environ.get('DATAPRESS_SCRIPT') is None:
            missing.append('DATAPRESS_SCRIPT')
        if missing:
            raise ValueError(f'Missing environment variables: {missing}')
        # --
        self.site_url = os.environ['DATAPRESS_URL']
        self.api_key = os.environ['DATAPRESS_API_KEY']
        self.dataset_id = os.environ['DATAPRESS_DATASET']
        self.script_id = os.environ['DATAPRESS_SCRIPT']
        # ---
        # Check the connection
        context = requests.get(self.site_url + '/api/context', headers={
            'Authorization': self.api_key
        })
        if (context.status_code != 200):
            raise Exception(
                f'Error connecting to DataPress: {r.status_code}')
        if context.json().get('user') is None and self.api_key is not None:
            raise Exception('Unrecognised API Key')
        # ---
        # Load the dataset
        # ---
        dataset = self.get_dataset()
        # Load the script
        if not self.script_id in dataset['scripts']:
            raise Exception(f'Script not found: {self.script_id}')
        logger.info('Connected to DataPress / dataset=%s / script=%s',
                    self.dataset_id, self.script_id)

    def get_dataset(self):
        r = requests.get(self.site_url + '/api/dataset/' + self.dataset_id, headers={
            'Authorization': self.api_key
        })
        if r.status_code != 200:
            raise Exception(f'Error fetching dataset: {r.status_code}')
        return r.json()

    def load_dataframe(self, dataset, resource_id):
        """
        Fetch this resource ID from the dataset and return it as a Pandas DataFrame.
        """
        if not resource_id in dataset['resources']:
            raise ValueError(
                f'Dataset does not contain resource {resource_id}')
        url = dataset['resources'][resource_id]['url']
        logger.debug('Loading resource %s from %s', resource_id, url)
        extension = os.path.splitext(url.lower())[1]
        # --
        r = requests.get(url + '?redirect=true', headers={
            'Authorization': self.api_key
        })
        if (r.status_code != 200):
            print(r.status_code)
            # If the response is json, print it
            try:
                # format the JSON nicely
                print(json.dumps(r.json(), indent=2))
            except:
                print(r.text)
            raise Exception(
                f'Error downloading resource from {url}: {r.status_code}')
        # Open a pandas dataframe:
        if extension == '.xlsx' or extension == '.xls':
            return pd.read_excel(io.BytesIO(r.content))
        elif extension == '.csv':
            return pd.read_csv(io.StringIO(r.text))
        else:
            # Unrecognised file type
            return None

    def load_dataframes(self):
        """
        Fetch DataPress files as pandas DataFrames.

        Loads all the resources listed on the script in the DataPress UI.
        (Indexed by filename and also by resource ID).
        """
        dataset = self.get_dataset()  #  Always refreshing this
        resource_ids = dataset['scripts'][self.script_id]['resources']
        dfz = {}
        for (i, id) in enumerate(resource_ids):
            url = dataset['resources'][id]['url']
            # Get the filename (decoding the URL)
            encoded_filename = url.split('/')[-1]
            filename = requests.utils.unquote(encoded_filename).lower()
            logger.info('Downloading file %d of %d: %s', i + 1,
                        len(resource_ids), filename)
            df = self.load_dataframe(dataset, resource_ids[i])
            if df is None:
                logger.info('Skipping unrecognised file type: %s', filename)
            else:
                dfz[filename] = df
                dfz[id] = df
        return dfz

    def _commit_csv(self, csv_data, name, type):
        """
        Private method: Upload a table or chart via a pre-signed link
        """
        if (type != 'chart' and type != 'table'):
            # Invalid value
            raise ValueError('Invalid type: %s' % type)

        # Request a presigned upload from the website, at
        # /api/dataset/:id/presign/script/:script_id/table/:table_id
        presign_url = '/'.join([
            self.site_url,
            'api',
            'dataset',
            self.dataset_id,
            'presign',
            'script',
            self.script_id,
            type,
            name,
        ])
        presign = requests.post(presign_url, headers={
            'Authorization': self.api_key
        }).json()

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

    def commit_table(self, name, df):
        """
        Upload a table to DataPress.
        Provide a kebab-case-name for the table, and a pandas dataframe.
        """
        # Fetch the dataset metadata
        dataset = self.get_dataset()
        tables = dataset['scripts'][self.script_id]['tables']
        csv_data = df.to_csv(index=False).encode('utf-8')

        # Deduplicate
        if name in tables:
            old_hash = tables[name]['csvHash']
            new_hash = hashlib.md5(csv_data).hexdigest()
            if old_hash == new_hash:
                logger.info('Skipping table: "%s" (CSV is unchanged)', name)
                return

        logger.info('Uploading table: "%s"', name)

        csv_key = self._commit_csv(csv_data, name, 'table')

        # Fetch the dataset metadata
        path = "/scripts/" + self.script_id + "/tables/" + name
        if name not in tables:
            logger.info('Creating table "%s" on the dataset', name)
            patch = [
                {   # Add the table
                    "op": "add",
                    "path": path,
                    "value": {'csv': csv_key}
                }
            ]
        else:
            logger.info('Updating table "%s" on the dataset', name)
            patch = [
                {   # Update the script's table key on DataPress
                    "op": "replace",
                    "path": path + '/csv',
                    "value": csv_key
                }
            ]
        # Send the patch request
        dataset_url = self.site_url + '/api/dataset/' + self.dataset_id
        r = requests.patch(dataset_url, headers={
            'Authorization': self.api_key},
            json=patch)
        if r.status_code != 200:
            print(r.json())
            raise Exception('Failed to update chart')

    def commit_chart(self, name, df):
        """
        Upload a table to DataPress.

        Provide a kebab-case-name for the table, and a pandas dataframe.
        The output CSV must be under 100kb.
        """
        # Refresh the dataset metadata
        dataset = self.get_dataset()
        charts = dataset['scripts'][self.script_id]['charts']
        csv_data = df.to_csv(index=False).encode('utf-8')

        # Deduplicate
        if name in charts:
            old_hash = charts[name]['csvHash']
            new_hash = hashlib.md5(csv_data).hexdigest()
            if old_hash == new_hash:
                logger.info('Skipping chart: "%s" (CSV is unchanged)', name)
                return

        # Verify we can chart this at all
        logger.info('Uploading chart: "%s"', name)
        if (len(csv_data) > 1024 * 100):
            raise Exception('Chart CSV data must be under 100kb')

        csv_key = self._commit_csv(csv_data, name, 'chart')

        path = "/scripts/" + self.script_id + "/charts/" + name
        if name not in charts:
            logger.info('Creating chart "%s" on the dataset', name)
            patch = [
                {   # Add the chart
                    "op": "add",
                    "path": path,
                    "value": {'csv': csv_key}
                }
            ]
        else:
            # Update the script's table key on DataPress
            logger.info('Updating chart "%s" on the dataset', name)
            patch = [
                {
                    "op": "replace",
                    "path": path + '/csv',
                    "value": csv_key
                }
            ]
        dataset_url = self.site_url + '/api/dataset/' + self.dataset_id
        r = requests.patch(dataset_url, headers={
            'Authorization': self.api_key},
            json=patch)
        if r.status_code != 200:
            print(r.json())
            raise Exception('Failed to update chart')
