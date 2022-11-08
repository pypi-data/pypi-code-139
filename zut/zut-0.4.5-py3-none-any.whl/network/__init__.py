from __future__ import annotations
import logging, os, re, urllib.request
from unittest import TestCase
from urllib.parse import unquote, urlparse
from .proxyconfig import SimpleProxyHandler, _proxy_configuration
from .socket import check_socket # zut.network API

try:
    from .windows import check_winhttp_connectivity
except ImportError:
    check_winhttp_connectivity = None

logger = logging.getLogger(__name__)

IP_ADDRESS_PATTERN = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

def detect_proxy_settings():
    # Detect proxy URL
    if "HTTP_PROXY" in os.environ:
        url = os.environ["HTTP_PROXY"]
    elif "http_proxy" in os.environ:
        url = os.environ["http_proxy"]
    else:
        return None

    # Detect proxy exclusions
    if "NO_PROXY" in os.environ:
        exclusions = os.environ["NO_PROXY"]
    elif "no_proxy" in os.environ:
        exclusions = os.environ["no_proxy"]
    else:
        exclusions = None

    # Parse proxy URL
    o = urlparse(url)
    m = re.match(r"^(?:(?P<username>[^\:]+)(?:\:(?P<password>[^\:]+))?@)?(?P<host>[^@\:]+)\:(?P<port>\d+)$", o.netloc)
    if not m:
        logger.error("cannot register proxy: invalid proxy netloc \"%s\"" % o.netloc)
        return None

    proxy_settings = {}
    proxy_settings["host"] = unquote(m.group("host")) if m.group("host") else None
    proxy_settings["port"] = int(m.group("port"))
    proxy_settings["username"] = unquote(m.group("username")) if m.group("username") else None
    proxy_settings["password"] = unquote(m.group("password")) if m.group("password") else None
    proxy_settings["scheme"] = o.scheme
    proxy_settings["exclusions"] = exclusions
    return proxy_settings            


def configure_proxy(**proxy_settings):
    """
    Configure proxy for urllib and winhttp (on windows) requests.
    """
    if not proxy_settings:
        proxy_settings = detect_proxy_settings()

    # Stop here if no proxy
    if not proxy_settings:
        return

    host = proxy_settings["host"]
    port = proxy_settings["port"]
    username = proxy_settings.get("username", None)
    password = proxy_settings.get("password", None)
    scheme = proxy_settings.get("scheme", "http")
    exclusions = proxy_settings.get("exclusions", None)

    _proxy_configuration.hostport = f"{host}:{port}"
    _proxy_configuration.exclusions = exclusions

    for key in ["HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"]:
        if key in os.environ:
            del os.environ[key]

    # Ensure no_proxy is specified (must be passed as environment variable for urllib)
    if exclusions:
        if isinstance(exclusions, list):
            exclusions = ",".join(exclusions)
        os.environ["NO_PROXY"] = exclusions

    # Register proxy for urllib
    try:
        _proxy_configuration.handler = SimpleProxyHandler(host=host, port=port, username=username, password=password, scheme=scheme)
        opener = urllib.request.build_opener(_proxy_configuration.handler)
        urllib.request.install_opener(opener)
    except Exception as e:
        logger.error("cannot register proxy for urllib: %s", e)


def get_proxy_url(for_url: str = None, include_password: bool = False):
    """
    Determine proxy URL.
    If `for_url` is given, return None if the proxy is excluded for this url.
    """
    if for_url:
        o = urlparse(for_url)
        if urllib.request.proxy_bypass(o.netloc if o.netloc else o.path):
            return None
    if not _proxy_configuration.handler:
        return None
    return _proxy_configuration.handler.get_proxy_url(include_password=include_password)


def check_urllib_connectivity(url: str, expected_regex: re.Pattern|str, label=None, timeout: float = None, case: TestCase = None) -> bool:
    """
    Test urllib connectivity.
    - `timeout`: in seconds (defaults to 3 seconds).

    Return True on success, False on failure.
    """        
    if not isinstance(expected_regex, re.Pattern):
        expected_regex = re.compile(expected_regex)

    if label is None:
        label = url

    if not timeout:
        timeout = float(os.environ.get("CHECK_CONNECTIVITY_TIMEOUT", 3))

    msg=f"{label} urllib"

    try:
        res = urllib.request.urlopen(url, timeout=timeout)
        text = res.read().decode('utf-8')
        text_startup = text[0:20].replace('\n', '\\n').replace('\r', '\\r') + ('…' if len(text) > 20 else '')
        
        if not expected_regex.match(text):
            failure = f"{msg}: response ({text_startup}) does not match regex ({expected_regex.pattern})"
            if case:
                case.fail(failure)
            else:
                logger.error(failure)
            return False

        logger.info(f"{msg}: success (response: {text_startup})")
        return True
    except urllib.error.URLError as e:
        failure = f"{msg}: {e.reason}"
        if case:
            case.fail(failure)
        else:
            logger.error(failure)
        return False


def check_connectivity(url: str, expected_regex: re.Pattern|str, label=None, timeout: float = None, case: TestCase = None) -> bool:
    """
    Test connectivity with urllib (and winhttp on Windows).
    - `timeout`: in seconds (defaults to 3 seconds).

    Return True on success, False on failure.
    """ 
    ok = check_urllib_connectivity(url, expected_regex, label=label, timeout=timeout, case=case)

    if check_winhttp_connectivity:
        ok = ok and check_winhttp_connectivity(url, expected_regex, label=label, timeout=timeout, case=case)

    return ok
