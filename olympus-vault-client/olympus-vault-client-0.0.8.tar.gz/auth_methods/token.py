import hvac

class Token():
    @staticmethod
    def login_token(vault_token,url):
        client = hvac.Client(url)
        client.token = vault_token
        return client
