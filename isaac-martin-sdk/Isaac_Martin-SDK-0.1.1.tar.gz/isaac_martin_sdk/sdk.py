import isaac_martin_sdk


class TheOneSDK:
    def __init__(self,
                 url: str = 'https://the-one-api.dev/v2',
                 authentication_token: str = None):
        '''
        :param url: The url for the api.
        :param authentication_token: An authentication token obtained here: https://the-one-api.dev/
        '''
        isaac_martin_sdk.sdk_config.API_URL = url
        isaac_martin_sdk.sdk_config.AUTHENTICATION_TOKEN = authentication_token
