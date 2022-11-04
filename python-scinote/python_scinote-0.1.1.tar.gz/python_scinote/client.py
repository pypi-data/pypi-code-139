import asyncio
import time

from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client


class SciNoteClient(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        server_url: str,
        token_saver: callable,
        code: str = None,
        refresh_token: str = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.server_url = server_url
        self.token_saver = token_saver
        self.code = code
        self.refresh_token = refresh_token
        self.access_token = None
        self.token = None

        self.initialize()

    def initialize(self):
        if self.token is None:
            if self.refresh_token:
                self.refresh_access_token()
            elif self.code:
                self.fetch_access_token()
            else:
                raise Exception("No code or refresh token provided")

    def fetch_access_token(self):
        client = OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        token = client.fetch_token(
            url=self.server_url + "/oauth/token",
            grant_type="authorization_code",
            code=self.code,
        )
        self.update_token(token)

    def refresh_access_token(self):
        client = OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        token = client.refresh_token(
            url=self.server_url + "/oauth/token",
            refresh_token=self.refresh_token,
        )
        self.update_token(token)

    def update_token(self, token):
        self.access_token = token["access_token"]
        self.refresh_token = token["refresh_token"]
        self.token = token
        self.token_saver(token)

    def sync_request(self, method, url):
        with OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=self.token,
            update_token=self.update_token,
        ) as client:
            return client.request(method, url)

    def async_request(self, method, url):
        with AsyncOAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=self.token,
            update_token=self.update_token,
        ) as client:
            return client.request(method, url)

    def get(self, url, mode="sync"):
        if mode == "sync":
            return self.sync_request("GET", url)
        elif mode == "async":
            return self.async_request("GET", url)

    def get_teams(self, without_emoji=False):
        url = self.server_url + "/api/v1/teams"
        r = self.get(url, mode="sync")
        r_json = r.json()

        while r.links.get("next"):
            r = self.get(r.links.get("next").get("url"), mode="sync")
            r_json.extend(r.json())

        teams_id_dict = {
            team["attributes"]["name"].replace("🟢 ", "")
            if without_emoji
            else team["attributes"]["name"]: team["id"]
            for team in r_json["data"]
            if "🟢" in team["attributes"]["name"]
        }

        return teams_id_dict

    def get_inventories(self, team_id):
        url = self.server_url + f"/api/v1/teams/{team_id}/inventories"
        r = self.get(url, mode="sync")
        r_json = r.json()

        while r.links.get("next"):
            r = self.get(r.links.get("next").get("url"), mode="sync")
            r_json.extend(r.json())

        inventories_id_dict = {
            inventory["attributes"]["name"]: inventory["id"]
            for inventory in r_json["data"]
        }

        return inventories_id_dict
