import requests

from .exceptions import StampHQClientError
from .models import Attachment

STAMPHQ_API_HOST = "https://api.stamphq.app/v1"
STAMPHQ_API_EMAIL_SEND = "email"

HDR_API_KEY = "x-stamphq-key"
HDR_CONTENT_TYPE = 'Content-Type'

ERR_API_KEY_NEEDED = "You need api_key to interact with stampHQ APIs."


class StampHQClient:
    """client class that initiates and sends email to stampHQ servers"""

    def __init__(self, api_key: str, max_retries=0):
        assert api_key, ERR_API_KEY_NEEDED
        self._api_key = api_key
        self.max_retries = max_retries
        if not hasattr(self, '_session'):
            self._session = requests.Session()  # pylint: disable=attribute-defined-outside-init
            adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)

    def send_email(
        self,
        sender: str,
        subject: str,
        text_content: str,
        html_content: str,
        attachments: list[Attachment] = None,
        to: list[str] = None,
        cc: list[str] = None,
        bcc: list[str] = None,
        headers: dict[str, str] = None,
    ) -> str:
        if attachments is None:
            attachments = []
        if to is None:
            to = []
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []
        assert sender, "`sender` address is mandatory"
        assert subject, "`subject` is mandatory"
        assert text_content or html_content or len(attachments), \
            "`text_content` or `html_content` or `attachments` are needed to send an email"

        payload = {
            'from': sender,
            'to': to,
            'cc': cc,
            'bcc': bcc,
            'subject': subject,
            'textContent': text_content,
            'htmlContent': html_content,
            'attachments': attachments,
            'headers': headers,
        }

        # call the API
        response = self._session.post(
            url='{}/{}'.format(STAMPHQ_API_HOST, STAMPHQ_API_EMAIL_SEND),
            headers={
                HDR_API_KEY: self._api_key,
            },
            json=payload,
        )
        try:
            response.raise_for_status()
            json = response.json()
            return json['messageId']
        except requests.HTTPError as http_error:
            try:
                data = response.json()
            except ValueError as exc:
                raise http_error from exc
            message = self.__format_exception_message(data)
            raise StampHQClientError(message, error_code=data["error"]) from http_error

    def __format_exception_message(self, data):
        return "[{}] {}".format(data["error"], data["message"])

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._api_key}, max_retries={self.max_retries}>"
