from __future__ import annotations
import re, os, logging, win32com.client, win32inetcon, pywintypes
from . import _proxy_configuration

logger = logging.getLogger(__name__)

def create_winhttp_request(timeout: float = None):
    """
    Create a winhttp request.
    - `timeout`: in seconds.
    """
    winhttp_req = win32com.client.Dispatch('WinHTTP.WinHTTPRequest.5.1')

    if timeout:
        winhttp_req.SetTimeouts(int(timeout*1000), int(timeout*1000), int(timeout*1000), int(timeout*1000))

    if _proxy_configuration.hostport:
        # See: https://docs.microsoft.com/en-us/windows/win32/winhttp/iwinhttprequest-setproxy
        # NOTE: no need to pass credentials, this is handled directly by Windows
        HTTPREQUEST_PROXYSETTING_DEFAULT   = 0
        HTTPREQUEST_PROXYSETTING_PRECONFIG = 0
        HTTPREQUEST_PROXYSETTING_DIRECT    = 1
        HTTPREQUEST_PROXYSETTING_PROXY     = 2
        winhttp_req.SetProxy(HTTPREQUEST_PROXYSETTING_PROXY, _proxy_configuration.hostport, _proxy_configuration.winhttp_exclusions)
        winhttp_req.SetAutoLogonPolicy(HTTPREQUEST_PROXYSETTING_DEFAULT)

    return winhttp_req


def check_winhttp_connectivity(url: str, expected_regex: re.Pattern|str, label=None, timeout: float = None) -> str:
    """
    Test winhttp connectivity.
    - `timeout`: in seconds (defaults to 3 seconds).
    
    Return a failure message (None on success).
    """        
    if not isinstance(expected_regex, re.Pattern):
        expected_regex = re.compile(expected_regex)

    if label is None:
        label = url

    if not timeout:
        timeout = float(os.environ.get("CHECK_CONNECTIVITY_TIMEOUT", 3))

    msg=f"{label} winhttp"

    winhttp_req = create_winhttp_request(timeout=timeout)
    winhttp_req.Open('GET', url, False)
    try:
        winhttp_req.Send()
        winhttp_req.WaitForResponse()
        if winhttp_req.Status != 200:
            failure = f"{msg}: {winhttp_req.Status} {winhttp_req.StatusText}"
            logger.error(failure)
            return failure

        text = winhttp_req.ResponseText
        text_startup = text[0:20].replace('\n', '\\n').replace('\r', '\\r') + ('…' if len(text) > 20 else '')

        if not expected_regex.match(text):
            failure = f"{msg}: response ({text_startup}) does not match regex ({expected_regex.pattern})"
            logger.error(failure)
            return failure
        
        logger.info(f"{msg}: success (response: {text_startup})")
        return None
    except pywintypes.com_error as e:
        if e.excepinfo[5] + 2**32 & 0xffff == win32inetcon.ERROR_INTERNET_TIMEOUT:
            details = "timed out"
        else:
            details = e.excepinfo[2].strip()
        failure = f"{msg}: {details}"
        logger.error(failure)
        return failure
