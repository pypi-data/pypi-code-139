from __future__ import annotations
import logging, os, socket, base64, re, urllib.request
from typing import Callable
from urllib.parse import quote, unquote, urlparse
from contextlib import closing
from unittest import TestCase

logger = logging.getLogger(__name__)

def check_socket(host, port, timeout=1):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        try:
            returncode = sock.connect_ex((host, port))
            if returncode == 0:
                return True
            else:
                logger.debug("socket connnect_ex returned %d", returncode)
                return False
        except Exception as e:
            logger.debug("socket connnect_ex: %s", e)
            return False


class SimpleProxyHandler(urllib.request.BaseHandler):
    # Inspired from urllib.request.ProxyHandler   
    handler_order = 100 # Proxies must be in front

    def __init__(self, host: str, port: str, username: str = None, password: str | Callable[[], str] = None, scheme: str = "http"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.scheme = scheme


    def finalize(self) -> str:
        # Determine password if this is a callable
        if self.password and isinstance(self.password, Callable):
            self.password = self.password()
        
        # Get proxy url (for logs)
        self.authorization = None
        proxy_logurl = self.get_proxy_url(include_password="*")
        logger.debug(f"use proxy for urllib: {proxy_logurl}")

        # Check proxy existency
        if not check_socket(self.host, self.port):
            logger.warning(f"cannot connect to proxy for urllib: {proxy_logurl}")

        # Prepare usefull variables for add_header and set_proxy
        self.hostport = f"{self.host}:{self.port}"

        if self.username:
            if not self.password:
                raise ValueError(f"missing password for urllib proxy: {proxy_logurl}")
            userpass = '%s:%s' % (self.username, self.password)
            self.authorization = "Basic " + base64.b64encode(userpass.encode()).decode("ascii")


    def get_proxy_url(self, include_password=False):
        if not hasattr(self, "authorization"):
            self.finalize()
        
        proxy_url = self.scheme + "://"

        if self.username:
            proxy_url += quote(self.username)

            if self.password:
                if include_password == "*":
                    proxy_url += ":" + ("*" * len(self.password))
                elif include_password:
                    proxy_url += ":" + quote(self.password)
            
            proxy_url += "@"

        proxy_url += f"{quote(self.host)}:{self.port}"
        return proxy_url


    def http_open(self, req):
        if not req.host:
            return None
        
        if urllib.request.proxy_bypass(req.host):
            # NOTE: because Proxy-Authorization header is not encrypted, we must add it ONLY when we're actually talking to the proxy
            return None

        if not hasattr(self, "authorization"):
            self.finalize()

        if self.authorization:
            req.add_header("Proxy-Authorization", self.authorization)
        req.set_proxy(self.hostport, self.scheme)
        return None
    

    def https_open(self, req):
        return self.http_open(req)


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



class _ProxyConfiguration:
    def __init__(self):
        self.handler: SimpleProxyHandler = None
        self.hostport: str = None
        self.exclusions: list[str] = None

    @property
    def winhttp_exclusions(self) -> str: 
        # NOTE: remove CIDR-block exclusions (not supported by WinHTTP)
        try:
            return self._winhttp_exclusions
        except:
            if self.exclusions:
                self._winhttp_exclusions = ",".join([exclusion for exclusion in _proxy_configuration.exclusions.split(",") if not "/" in exclusion])
            else:
                logger.warning("no exclusions for proxy: missing NO_PROXY environment variable?")
                self._winhttp_exclusions = "localhost"

            return self._winhttp_exclusions


_proxy_configuration = _ProxyConfiguration()


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


def test_urllib_request(case: TestCase, url: str, expected_regex: str, label=None, timeout: int = 2) -> str:
    if label is None:
        label = url
    msg=f"{label} urllib"

    try:
        res = urllib.request.urlopen(url, timeout=timeout)
        text = res.read().decode('utf-8')
        case.assertRegex(text, expected_regex, msg=msg)
    except urllib.error.URLError as e:
        case.fail(f"{msg}: {e.reason}")
