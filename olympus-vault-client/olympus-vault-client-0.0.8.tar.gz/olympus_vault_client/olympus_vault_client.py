import hvac

from auth_methods.token import Token

class OlympusVaultClient:
    def __init__(self
                 ):
        self.url = 'https://vault.prod.data-engineering.myteksi.net:443/'

    def read_secret(self,secret_path,key):
        try:
            from pyspark.dbutils import DBUtils
            # In Databricks
            dbutils = DBUtils()
            team = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get().split('/')[1]
            vault_token = dbutils.secrets.get(team,team+'-vault-token')

            client = Token.login_token(vault_token,self.url)
            read_response = client.secrets.kv.read_secret(path='databricks/'+team+'/'+secret_path)

            return read_response['data'][key]

        except ImportError:
            # In Chimera
            import IPython
            # dbutils = IPython.get_ipython().user_ns["dbutils"]

