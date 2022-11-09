from urllib3 import PoolManager, HTTPResponse
import json
import machineid


API_URL = 'https://api.playerloop.io'
REPORTS_URL = API_URL + '/reports'
ATTACHMENTS_URL = REPORTS_URL + '/%s/attachements'


# playerloop api docs
# https://playerloop.notion.site/Playerloop-Documentation-3f5d9f8d6e4043719222a4718dc16037#441941af00ea417cb584f64208f07ff9


class PlayerLoop:
    def __init__(self, secret:str, app_id:str='playerloop') -> None:
        # required fields
        self._secret = secret
        self.app_id = app_id

        # optional fields
        self.handle = ''
        self.email = ''

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': secret,
        }

        self.machine_id = machineid.hashed_id(app_id=app_id)

        self.http = PoolManager()
        self.last_response = None

    def send_report(self, message: str) -> HTTPResponse:
        """
        Send a report to Playerloop.

        Does not currently support file attachments.
        """
        data = {
            'text': message,
            'type': 'bug',
            'accepted_privacy' : True,
            'client' : 'custom',
            'player' : {
                'id' : self.machine_id,
            },
        }

        if self.handle:
            data['player']['handle'] = self.handle

        if self.email:
            data['player']['email'] = self.email

        body = json.dumps(data)

        r = self.http.request('POST', REPORTS_URL, headers=self.headers, body=body)
        self.last_response = r
        
    #     if r.status < 300:
    #         r_data = json.loads(r.data.decode())
    #         pid = r_data['data']['id']

        return r

    # def send_file(self):
    #     pass