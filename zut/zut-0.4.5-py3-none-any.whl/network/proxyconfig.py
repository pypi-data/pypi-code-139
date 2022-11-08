from __future__ import annotations
import base64, urllib.request, logging
from typing import Callable
from urllib.parse import quote

logger = logging.getLogger(__name__)

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

