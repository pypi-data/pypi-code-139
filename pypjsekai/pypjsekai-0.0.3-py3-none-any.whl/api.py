# SPDX-FileCopyrightText: 2022-present Erik Chan <erikchan002@gmail.com>
#
# SPDX-License-Identifier: MIT

from contextlib import contextmanager
from typing import Dict, List, Optional
from requests import Session
from uuid import uuid4
from jwt import encode as jwtEncode

from pjsekai.models import SystemInfo
from pjsekai.models import GameVersion
from pjsekai.asset_bundle import AssetBundle
from pjsekai.exceptions import *
from pjsekai.enums.tutorial_status import TutorialStatus
from pjsekai.enums.platform import Platform
from pjsekai.utilities import encrypt, decrypt, msgpack, unmsgpack

class API:

    platform: Platform
    domains: Dict[str, str]
    key: bytes
    iv : bytes
    jwt_secret: str
    system_info: SystemInfo
    enable_encryption: Dict[str,bool]
    game_version: GameVersion

    _session: Session
    @property
    def session(self) -> Session:
        return self._session

    _session_token: Optional[str]

    _api_domain: str
    @property
    def api_domain(self) -> str:
        try:
            return self._api_domain.format(self.game_version.profile)
        except IndexError:
            return self._api_domain
    @api_domain.setter
    def api_domain(self, new_value):
        self._api_domain = new_value
    _asset_bundle_domain: str
    @property
    def asset_bundle_domain(self) -> str:
        try:
            return self._asset_bundle_domain.format(self.game_version.profile, self.game_version.asset_bundle_host_hash)
        except IndexError:
            return self._asset_bundle_domain
    @asset_bundle_domain.setter
    def asset_bundle_domain(self, new_value):
        self._asset_bundle_domain = new_value
    _asset_bundle_info_domain: str
    @property
    def asset_bundle_info_domain(self) -> str:
        try:
            return self._asset_bundle_info_domain.format(self.game_version.profile, self.game_version.asset_bundle_host_hash)
        except IndexError:
            return self._asset_bundle_info_domain
    @asset_bundle_info_domain.setter
    def asset_bundle_info_domain(self, new_value):
        self._asset_bundle_info_domain = new_value
    _game_version_domain: str
    @property
    def game_version_domain(self) -> str:
        try:
            return self._game_version_domain.format(self.game_version.profile)
        except IndexError:
            return self._game_version_domain
    @game_version_domain.setter
    def game_version_domain(self, new_value):
        self._game_version_domain = new_value
    _signature_domain: str
    @property
    def signature_domain(self) -> str:
        try:
            return self._signature_domain.format(self.game_version.profile)
        except IndexError:
            return self._signature_domain
    @signature_domain.setter
    def signature_domain(self, new_value):
        self._signature_domain = new_value

    enable_api_encryption: bool
    enable_asset_bundle_encryption: bool
    enable_asset_bundle_info_encryption: bool
    enable_game_version_encryption: bool
    enable_signature_encryption: bool

    DEFAULT_API_DOMAIN: str = "production-game-api.sekai.colorfulpalette.org"
    DEFAULT_ASSET_BUNDLE_DOMAIN: str = "{0}-{1}-assetbundle.sekai.colorfulpalette.org"
    DEFAULT_ASSET_BUNDLE_INFO_DOMAIN: str = "{0}-{1}-assetbundle-info.sekai.colorfulpalette.org"
    DEFAULT_GAME_VERSION_DOMAIN: str = "game-version.sekai.colorfulpalette.org"
    DEFAULT_SIGNATURE_DOMAIN: str =  "issue.sekai.colorfulpalette.org"

    DEFAULT_ENABLE_API_ENCRYPTION: bool = True
    DEFAULT_ENABLE_ASSET_BUNDLE_ENCRYPTION: bool = False
    DEFAULT_ENABLE_ASSET_BUNDLE_INFO_ENCRYPTION: bool = True
    DEFAULT_ENABLE_GAME_VERSION_ENCRYPTION: bool = True
    DEFAULT_ENABLE_SIGNATURE_ENCRYPTION: bool = True

    DEFAULT_CHUNK_SIZE: int = 1024 * 1024

    def __init__(
        self, 
        platform: Platform, 
        key: bytes, 
        iv: bytes, 
        jwt_secret: str, 
        system_info: Optional[SystemInfo],
        api_domain: str,
        asset_bundle_domain: str,
        asset_bundle_info_domain: str,
        game_version_domain: str,
        signature_domain: str,
        enable_api_encryption: bool,
        enable_asset_bundle_encryption: bool,
        enable_asset_bundle_info_encryption: bool,
        enable_game_version_encryption: bool,
        enable_signature_encryption: bool,
    ) -> None:
        self.platform = platform
        self._session = Session()
        self.key = key
        self.iv = iv
        self.jwt_secret = jwt_secret
        self.system_info = SystemInfo()
        if system_info is not None:
            self.system_info = system_info
        self.api_domain = api_domain
        self._asset_bundle_domain = asset_bundle_domain
        self._asset_bundle_info_domain = asset_bundle_info_domain
        self._game_version_domain = game_version_domain
        self._signature_domain = signature_domain
        self.enable_api_encryption = enable_api_encryption
        self.enable_asset_bundle_encryption = enable_asset_bundle_encryption
        self.enable_asset_bundle_info_encryption = enable_asset_bundle_info_encryption
        self.enable_game_version_encryption = enable_game_version_encryption
        self.enable_signature_encryption = enable_signature_encryption

        self._session_token = None
        self.game_version = GameVersion()

    def _pack(self, plaintext_dict: Optional[dict], enable_encryption: bool = True) -> bytes:
        plaintext: bytes = msgpack(plaintext_dict)
        return encrypt(plaintext, self.key, self.iv) if enable_encryption else plaintext

    def _unpack(self, ciphertext: bytes, enable_decryption: bool = True) -> dict:
        plaintext: bytes = decrypt(ciphertext, self.key, self.iv) if enable_decryption else ciphertext
        return unmsgpack(plaintext)

    def _generate_headers(self, system_info: Optional[SystemInfo] = None) -> dict:
        app_version: Optional[str]
        data_version: Optional[str]
        asset_version: Optional[str]
        if system_info is None:
            app_version = self.system_info.app_version
            data_version = self.system_info.data_version
            asset_version = self.system_info.asset_version
        else:
            app_version = system_info.app_version
            data_version = system_info.data_version
            asset_version = system_info.asset_version
        return {
            "Content-Type": "application/octet-stream",
            "Accept": "application/octet-stream",
            "X-App-Version": app_version,
            "X-Data-Version": data_version,
            "X-Asset-Version": asset_version,
            "X-Request-Id": str(uuid4()),
            "X-Unity-Version": self.platform.unity_version,
            
            **({} if self._session_token is None else {
                "X-Session-Token": self._session_token,
            }),
            **self.platform.headers,
        }

    def get_signed_cookie(self, system_info: Optional[SystemInfo] = None) -> str:
        url: str = f"https://{self.signature_domain}/api/signature"
        encrypt: bool = self.enable_signature_encryption
        with self.session.post(
            url,
            headers=self._generate_headers(system_info),
            data=self._pack(None,encrypt),
        ) as response:
            response.raise_for_status()
            return response.headers["Set-Cookie"]

    def get_game_version(self, app_version: Optional[str] = None, app_hash: Optional[str] = None, system_info: Optional[SystemInfo] = None) -> dict:
        if app_version is None:
            if system_info is None:
                app_version = self.system_info.app_version
            else:
                app_version = system_info.app_version
        if app_hash is None:
            if system_info is None:
                app_hash = self.system_info.app_hash
            else:
                app_hash = system_info.app_hash
        url: str = f"https://{self.game_version_domain}/{app_version}/{app_hash}"
        encrypt: bool = self.enable_game_version_encryption
        with self.session.get(
            url,
            headers=self._generate_headers(system_info),
        ) as response:
            response.raise_for_status()
            return self._unpack(response.content, encrypt)

    def get_asset_bundle_info(self, asset_version: Optional[str] = None, system_info: Optional[SystemInfo] = None) -> dict:
        if asset_version is None:
            if system_info is None:
                asset_version = self.system_info.asset_version
            else:
                asset_version = system_info.asset_version
        url: str = f"https://{self.asset_bundle_info_domain}/api/version/{asset_version}/os/{self.platform.asset_os.value}"
        encrypt: bool = self.enable_asset_bundle_info_encryption
        with self.session.get(url,headers=self._generate_headers(system_info)) as response:
            if response.status_code == 426:
                raise UpdateRequired
            elif response.status_code == 403:
                raise SessionExpired
            response.raise_for_status()
            return self._unpack(response.content, encrypt)

    @contextmanager
    def download_asset_bundle(self, asset_bundle_name: str, chunk_size: Optional[int] = None, system_info: Optional[SystemInfo] = None):
        if chunk_size is None:
            chunk_size = self.DEFAULT_CHUNK_SIZE
        asset_version: Optional[str] = self.system_info.asset_version
        asset_hash: Optional[str] = self.system_info.asset_hash
        if system_info is not None:
            asset_version = system_info.asset_version
            asset_hash = system_info.asset_hash
        if asset_version is None or asset_hash is None:
            raise UpdateRequired
        url: str = f"https://{self.asset_bundle_domain}/{asset_version}/{asset_hash}/android/{asset_bundle_name}"
        encrypt: bool = self.enable_asset_bundle_encryption
        if encrypt:
            raise NotImplementedError
        response = self.session.get(url, stream=True)
        try:
            if response.status_code == 426:
                raise UpdateRequired
            elif response.status_code == 403:
                raise SessionExpired
            response.raise_for_status()
            yield AssetBundle(obfuscated_chunks=response.iter_content(chunk_size=chunk_size))
        finally:
            response.close()

    def request(
        self, 
        method: str, 
        path: str, 
        params: Optional[dict] = None, 
        data: Optional[dict] = None, 
        headers: Optional[dict] = None, 
        system_info: Optional[SystemInfo] = None
    ) -> dict:
        url: str = f"https://{self.api_domain}/api/{path}"
        encrypt: bool = self.enable_api_encryption
        with self.session.request(
            method,
            url,
            headers={
                **self._generate_headers(system_info),
                **({} if headers is None else headers),
            },
            params=params,
            data=self._pack(data,encrypt) if data is not None or method.casefold()=="POST".casefold() else None
        ) as response:
            if response.status_code == 426:
                raise UpdateRequired
            elif response.status_code == 403:
                raise SessionExpired
            response.raise_for_status()
            self._session_token = response.headers.get("X-Session-Token", self._session_token)
            return self._unpack(response.content,encrypt)
    
    def ping(self) -> dict:
        return self.request("GET","")

    def get_system_info(self) -> dict:
        return self.request("GET", "system")
    
    def register(self) -> dict:
        return self.request("POST", "user", data = self.platform.info)

    def authenticate(self, user_id: str, credential: str) -> dict:
        responseDict: dict = self.request("PUT", f"user/{user_id}/auth", data = { "credential": credential })
        self._session_token = responseDict["sessionToken"]
        return responseDict

    def get_master_data(self, data_version: Optional[str] = None) -> dict:
        if data_version is None:
            return self.request("GET", f"suite/master")
        else:
            return self.request("GET", f"suite/master", system_info=self.system_info.copy(update={"dataVersion":data_version}))

    def get_notices(self) -> dict:
        return self.request("GET", f"information")

    def get_user_data(self, user_id: str, name: Optional[str] = None) -> dict:
        params = {
            "isForceAllReload": name is None,
            "name": name,
        }
        return self.request("GET", f"suite/user/{user_id}", params=params)
    
    def get_login_bonus(self, user_id: str) -> dict:
        return self.request("PUT", f"user/{user_id}/home/refresh", data = {
            "refreshableTypes":[
                "new_pending_friend_request",
                "login_bonus"
            ]
        })

    def get_profile(self, user_id: str) -> dict:
        return self.request("GET", f"user/{user_id}/profile")

    def set_tutorial_status(self, user_id: str, tutorial_status: TutorialStatus) -> dict:
        return self.request("PATCH", f"user/{user_id}/tutorial", data = { "tutorialStatus": tutorial_status.value })

    def generate_transfer_code(self, user_id: str, password: str) -> dict:
        return self.request("PUT", f"user/{user_id}/inherit", data = { "password": password })

    def checkTransferCode(self, transfer_code: str, password: str) -> dict:
        token_payload = {
            "inheritId": transfer_code,
            "password": password
        }
        header = {
            "x-inherit-id-verify-token": jwtEncode(token_payload, self.jwt_secret, algorithm="HS256"),
        }
        params = {
            "isExecuteInherit": False,
        }
        return self.request("POST", f"inherit/user/{transfer_code}", params=params, headers=header)

    def generate_credential(self, transfer_code: str, password: str) -> dict:
        token_payload = {
            "inheritId": transfer_code,
            "password": password
        }
        header = {
            "x-inherit-id-verify-token": jwtEncode(token_payload, self.jwt_secret, algorithm="HS256"),
        }
        params = {
            "isExecuteInherit": True,
        }
        return self.request("POST", f"inherit/user/{transfer_code}", params=params, headers=header)

    def gacha(self, user_id: str, gacha_id: int, gacha_behavior_id: int) -> dict:
        return self.request("PUT", f"user/{user_id}/gacha/{gacha_id}/gachaBehaviorId/{gacha_behavior_id}")

    def receive_presents(self, user_id: str, present_ids: List[str]) -> dict:
        return self.request("POST", f"user/{user_id}/present", data = {
            "presentIds": present_ids
        })

    def start_solo_live(
        self, 
        user_id: str, 
        music_id: int, 
        music_difficulty_id: int, 
        music_vocal_id: int, 
        deck_id: int, 
        boost_count: int, 
        is_auto: bool
    ) -> dict:
        return self.request("POST", f"user/{user_id}/live", data = {
            "musicId": music_id,
            "musicDifficultyId": music_difficulty_id,
            "musicVocalId": music_vocal_id,
            "deckId": deck_id,
            "boostCount": boost_count,
            "isAuto": is_auto
        })

    def end_solo_live(
        self, 
        user_id: str, 
        live_id:str, 
        score: int, 
        perfect_count: int, 
        great_count: int, 
        good_count: int, 
        bad_count: int, 
        miss_count: int, 
        max_combo: int, 
        life: int, 
        tap_count: int, 
        continue_count: int
    ) -> dict:
        return self.request("PUT", f"user/{user_id}/live/{live_id}", data = {
            "score": score,
            "perfectCount": perfect_count,
            "greatCount": great_count,
            "goodCount": good_count,
            "badCount": bad_count,
            "missCount": miss_count,
            "maxCombo": max_combo,
            "life": life,
            "tapCount": tap_count,
            "continueCount": continue_count
        })

    def get_event_rankings(
        self, 
        user_id: str, 
        event_id: int, 
        target_user_id: Optional[str] = None, 
        target_rank: Optional[int] = None, 
        higher_limit: Optional[int] = None, 
        lower_limit: Optional[int] = None
    ) -> dict:
        if target_user_id is None and target_rank is None:
            target_user_id = user_id
        params = {
            "targetUserId": target_user_id,
            "targetRank": target_rank,
            "higherLimit": higher_limit,
            "lowerLimit": lower_limit,
        }
        return self.request("GET", f"user/{user_id}/event/{event_id}/ranking", params=params)

    def get_event_teams_player_count(self, event_id: int) -> dict:
        return self.request("GET", f"cheerful-carnival-team-count/{event_id}")

    def get_event_teams_point(self, event_id: int) -> dict:
        return self.request("GET", f"cheerful-carnival-team-point/{event_id}")

    def get_rank_match_rankings(
        self, 
        user_id: str, 
        rank_match_season_id: int, 
        target_user_id: Optional[str] = None, 
        target_rank: Optional[int] = None, 
        higher_limit: Optional[int] = None, 
        lower_limit: Optional[int] = None
    ) -> dict:
        if target_user_id is None and target_rank is None:
            target_user_id = user_id
        params = {
            "targetUserId": target_user_id,
            "targetRank": target_rank,
            "higherLimit": higher_limit,
            "lowerLimit": lower_limit,
        }
        return self.request("GET", f"user/{user_id}/rank-match-season/{rank_match_season_id}/ranking", params=params)

    def get_room_invitations(self, user_id: str) -> dict:
        return self.request("GET", f"user/{user_id}/invitation")
    
    def send_friend_request(self, user_id: str, target_user_id: str, message: Optional[str] = None) -> dict:
        return self.request("POST", f"user/{user_id}/friend/{target_user_id}", data={
            "message": message, 
            "friendRequestSentLocation": "id_search",
        })

    def reject_friend_request(self, user_id: str, request_user_id: str) -> dict:
        params = {
            "type": "reject_friend_request",
        }
        return self.request("DELETE", f"user/{user_id}/friend/{request_user_id}", params=params)

    def accept_friend_request(self, user_id: str, request_user_id: str) -> dict:
        return self.request("PUT", f"user/{user_id}/friend/{request_user_id}")

    def remove_friend(self, user_id: str, friend_user_id: str) -> dict:
        params = {
            "type": "release_friend",
        }
        return self.request("DELETE", f"user/{user_id}/friend/{friend_user_id}", params=params)
