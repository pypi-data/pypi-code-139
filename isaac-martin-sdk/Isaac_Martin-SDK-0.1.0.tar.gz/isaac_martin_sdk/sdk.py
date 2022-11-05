import isaac_martin_sdk

class TheOneSDK:
    def __init__(self, url: str, authentication_token: str):
        isaac_martin_sdk.sdk_config.API_URL = url
        isaac_martin_sdk.sdk_config.AUTHENTICATION_TOKEN = authentication_token
