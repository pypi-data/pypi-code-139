import gettext
import os
import json

from contextlib import suppress

from aiohttp import ClientSession

from typing import Dict
from asyncytmusicapi.helpers import (
    initialize_headers,
    initialize_context,
    get_visitor_id,
    get_authorization,
    sapisid_from_cookie,
    locale,
)
from asyncytmusicapi.constants import YTM_BASE_API, YTM_PARAMS

from asyncytmusicapi.parsers import browsing
from asyncytmusicapi.setup import setup
from asyncytmusicapi.mixins.browsing import BrowsingMixin
from asyncytmusicapi.mixins.search import SearchMixin
from asyncytmusicapi.mixins.watch import WatchMixin
from asyncytmusicapi.mixins.explore import ExploreMixin
from asyncytmusicapi.mixins.library import LibraryMixin
from asyncytmusicapi.mixins.playlists import PlaylistsMixin
from asyncytmusicapi.mixins.uploads import UploadsMixin


class YTMusic(
    BrowsingMixin,
    SearchMixin,
    WatchMixin,
    ExploreMixin,
    LibraryMixin,
    PlaylistsMixin,
    UploadsMixin,
):
    """
    Allows automated interactions with YouTube Music by emulating the YouTube web client's requests.
    Permits both authenticated and non-authenticated requests.
    Authentication header data must be provided on initialization.
    """

    def __init__(
        self,
        auth: str = None,
        user: str = None,
        proxies: dict = None,
        language: str = "en",
    ):
        self.auth = auth
        self.proxies = proxies
        self.cookies = {"CONSENT": "YES+1"}
        self.headers = initialize_headers()
        self.context = initialize_context()
        self.context["context"]["client"]["hl"] = language

        locale_dir = os.path.abspath(os.path.dirname(__file__)) + os.sep + "locales"
        supported_languages = [f for f in next(os.walk(locale_dir))[1]]
        if language not in supported_languages:
            raise Exception(
                "Language not supported. Supported languages are "
                + (", ".join(supported_languages))
                + "."
            )
        self.language = language
        try:
            locale.setlocale(locale.LC_ALL, self.language)
        except locale.Error:
            with suppress(locale.Error):
                locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.lang = gettext.translation(
            "base", localedir=locale_dir, languages=[language]
        )
        self.parser = browsing.Parser(self.lang)

        if user:
            self.context["context"]["user"]["onBehalfOfUser"] = user

        # verify authentication credentials work
        if auth:
            try:
                cookie = self.headers.get("cookie")
                self.sapisid = sapisid_from_cookie(cookie)
            except KeyError:
                raise Exception(
                    "Your cookie is missing the required value __Secure-3PAPISID"
                )

    async def update_headers(self):
        self.headers.update(await get_visitor_id(self._send_get_request))

    async def _send_request(
        self, endpoint: str, body: Dict, additionalParams: str = ""
    ) -> Dict:
        if "x-goog-visitor-id" not in self.headers:
            await self.update_headers()
        body.update(self.context)
        if self.auth:
            origin = self.headers.get("origin", self.headers.get("x-origin"))
            self.headers["Authorization"] = get_authorization(
                self.sapisid + " " + origin
            )

        session = ClientSession()
        url = YTM_BASE_API + endpoint + YTM_PARAMS + additionalParams
        response = await session.post(
            json=body,
            url=url,
            headers=self.headers,
            proxy=self.proxies,
            cookies=self.cookies,
        )
        response_text = json.loads(await response.text())
        await session.close()
        if response.status >= 400:
            message = (
                "Server returned HTTP "
                + str(response.status)
                + ": "
                + response.reason
                + ".\n"
            )
            error = response_text.get("error", {}).get("message")
            raise Exception(message + error)

        return response_text

    async def _send_get_request(self, url: str, params: Dict = None):
        session = ClientSession()
        response = await session.get(
            url,
            params=params,
            headers=self.headers,
            proxy=self.proxies,
            cookies=self.cookies,
        )
        response = await response.text()
        await session.close()
        return response

    def _check_auth(self):
        if not self.auth:
            raise Exception("Please provide authentication before using this function")

    @classmethod
    def setup(cls, filepath: str = None, headers_raw: str = None) -> Dict:
        """
        Requests browser headers from the user via command line
        and returns a string that can be passed to YTMusic()

        :param filepath: Optional filepath to store headers to.
        :param headers_raw: Optional request headers copied from browser.
            Otherwise requested from terminal
        :return: configuration headers string
        """
        return setup(filepath, headers_raw)

    def __enter__(self):
        return self

    def __exit__(self, execType=None, execValue=None, trackback=None):
        pass
