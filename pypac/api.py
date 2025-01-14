"""
These are the most commonly used components of PyPAC.
"""
import os
from contextlib import contextmanager

import requests
from requests.exceptions import ProxyError, ConnectTimeout

from time import sleep
from pypac.parser import PACFile
from pypac.resolver import ProxyResolver, ProxyConfigExhaustedError
from pypac.os_settings import autoconfig_url_from_registry, autoconfig_url_from_preferences, \
    ON_WINDOWS, ON_DARWIN, file_url_to_local_path
from pypac.wpad import proxy_urls_from_dns


def get_pac(url=None, js=None, from_os_settings=True, from_dns=True, timeout=2,
            allowed_content_types=None, session=None, **kwargs):
    """
    Convenience function for finding and getting a parsed PAC file (if any) that's ready to use.

    :param str url: Download PAC from a URL.
        If provided, `from_os_settings` and `from_dns` are ignored.
    :param str js: Parse the given string as a PAC file.
        If provided, `from_os_settings` and `from_dns` are ignored.
    :param bool from_os_settings: Look for a PAC URL or filesystem path from the OS settings, and use it if present.
        Doesn't do anything on non-Windows or non-macOS/OSX platforms.
    :param bool from_dns: Look for a PAC file using the WPAD protocol.
    :param timeout: Time to wait for host resolution and response for each URL.
    :param allowed_content_types: If the response has a ``Content-Type`` header,
        then consider the response to be a PAC file only if the header is one of these values.
        If not specified, the allowed types are
        ``application/x-ns-proxy-autoconfig`` and ``application/x-javascript-config``.
    :return: The first valid parsed PAC file according to the criteria, or `None` if nothing was found.
    :rtype: PACFile|None
    :raises MalformedPacError: If something that claims to be a PAC file was obtained but could not be parsed.
    """
    if url:
        downloaded_pac = download_pac([url], timeout=timeout,
                                      allowed_content_types=allowed_content_types,
                                      session=session)
        if not downloaded_pac:
            return
        return PACFile(downloaded_pac, **kwargs)
    if js:
        return PACFile(js, **kwargs)

    # Deprecated in 0.8.2
    from_registry = kwargs.get('from_registry')
    if from_registry is not None:
        import warnings
        warnings.warn('from_registry is deprecated, use from_os_settings instead.')
        from_os_settings = from_registry

    if from_os_settings:
        if ON_WINDOWS:
            path = autoconfig_url_from_registry()
        elif ON_DARWIN:
            path = autoconfig_url_from_preferences()
        else:
            path = None

        if path and path.lower().startswith('file://'):
            path = file_url_to_local_path(path)

        if path and os.path.isfile(path):
            with open(path) as f:
                return PACFile(f.read(), **kwargs)

    pac_candidate_urls = collect_pac_urls(from_os_settings=True, from_dns=from_dns)
    downloaded_pac = download_pac(pac_candidate_urls, timeout=timeout, allowed_content_types=allowed_content_types, session=session)
    if not downloaded_pac:
        return
    return PACFile(downloaded_pac, **kwargs)


def collect_pac_urls(from_os_settings=True, from_dns=True, **kwargs):
    """
    Get all the URLs that potentially yield a PAC file.

    :param bool from_os_settings: Look for a PAC URL from the OS settings.
        If a value is found and is a URL, it comes first in the returned list.
        Doesn't do anything on non-Windows or non-macOS/OSX platforms.
    :param bool from_dns: Assemble a list of PAC URL candidates using the WPAD protocol.
    :return: A list of URLs that should be tried in order.
    :rtype: list[str]
    """
    # Deprecated in 0.8.2
    from_registry = kwargs.get('from_registry')
    if from_registry is not None:
        import warnings
        warnings.warn('from_registry is deprecated, use from_os_settings instead.')
        from_os_settings = from_registry

    pac_urls = []
    if from_os_settings:
        if ON_WINDOWS:
            url_or_path = autoconfig_url_from_registry()
        elif ON_DARWIN:
            url_or_path = autoconfig_url_from_preferences()
        else:
            url_or_path = None

        if url_or_path and (url_or_path.lower().startswith('http://') or url_or_path.lower().startswith('https://')):
            pac_urls.append(url_or_path)
    if from_dns:
        pac_urls.extend(proxy_urls_from_dns())
    return pac_urls


def download_pac(candidate_urls, timeout=1, allowed_content_types=None,
                 session=None):
    """
    Try to download a PAC file from one of the given candidate URLs.

    :param list[str] candidate_urls: URLs that are expected to return a PAC file.
        Requests are made in order, one by one.
    :param timeout: Time to wait for host resolution and response for each URL.
        When a timeout or DNS failure occurs, the next candidate URL is tried.
    :param allowed_content_types: If the response has a ``Content-Type`` header,
        then consider the response to be a PAC file only if the header is one of these values.
        If not specified, the allowed types are
        ``application/x-ns-proxy-autoconfig`` and ``application/x-javascript-config``.
    :return: Contents of the PAC file, or `None` if no URL was successful.
    :rtype: str|None
    """
    if not allowed_content_types:
        allowed_content_types = {'application/x-ns-proxy-autoconfig', 'application/x-javascript-config'}

    if not session:
        sess = requests.Session()
    else:
        sess = session
    sess.trust_env = False  # Don't inherit proxy config from environment variables.
    for pac_url in candidate_urls:
        try:
            resp = sess.get(pac_url, timeout=timeout)
            content_type = resp.headers.get('content-type', '').lower()
            if content_type and True not in [allowed_type in content_type for allowed_type in allowed_content_types]:
                continue
            if resp.ok:
                return resp.text
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            PrintException()
            continue
import random
import sys, linecache
def PrintException( ):
    #if apiKey == firstkey:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    string = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    if 'connect timeout' not in string and 'Read timed out' not in string:
        print(string)
class PACSession(requests.Session):
    """
    A PAC-aware :ref:`Requests Session <requests:session-objects>` that discovers and complies with a PAC file,
    without any configuration necessary. PAC file discovery is accomplished via the Windows Registry (if applicable),
    and the Web Proxy Auto-Discovery (WPAD) protocol. Alternatively, a PAC file may be provided in the constructor.
    """

    def __init__(self, pac=None, proxy_auth=None, pac_enabled=True,
                 response_proxy_fail_filter=None, exception_proxy_fail_filter=None,
                 socks_scheme='socks5', masterproxies=None, **kwargs):
        """
        :param PACFile pac: The PAC file to consult for proxy configuration info.
            If not provided, then upon the first request, :func:`get_pac` is called with default arguments
            in order to find a PAC file.
        :param requests.auth.HTTPProxyAuth proxy_auth: Username and password proxy authentication.
        :param bool pac_enabled: Set to ``False`` to disable all PAC functionality, including PAC auto-discovery.
        :param response_proxy_fail_filter: Callable that takes a ``requests.Response`` and returns
            a boolean for whether the response means the proxy used for the request should no longer be used.
            By default, the response is not inspected.
        :param exception_proxy_fail_filter: Callable that takes an exception and returns
            a boolean for whether the exception means the proxy used for the request should no longer be used.
            By default, :class:`requests.exceptions.ConnectTimeout` and
            :class:`requests.exceptions.ProxyError` are matched.
        :param str socks_scheme: Scheme to use when PAC file returns a SOCKS proxy. `socks5` by default.
        """
        super(PACSession, self).__init__()
        self._tried_get_pac = False
        self.masterproxies = masterproxies
        #print(self.masterproxies)
        self._proxy_resolver = None
        self._proxy_auth = proxy_auth
        self._socks_scheme = socks_scheme

        if kwargs.get('recursion_limit'):
            import warnings
            warnings.warn('recursion_limit is deprecated and has no effect. It will be removed in a future release.')

        #: Set to ``False`` to disable all PAC functionality, including PAC auto-discovery.
        self.pac_enabled = pac_enabled
        #print(2)
        
        #print(pac)
        if pac:
            #print(3)
            #self._tried_get_pac = True
            self._proxy_resolver = self._get_proxy_resolver(pac)
        self.proxies2 = []
        self._response_proxy_failure_filter = default_proxy_fail_response_filter
        self.response_proxy_fail_filter = response_proxy_fail_filter
        if response_proxy_fail_filter:
            self._response_proxy_failure_filter = response_proxy_fail_filter
        self.default_proxy_fail_exception_filter = default_proxy_fail_exception_filter
        self._exc_proxy_failure_filter = default_proxy_fail_exception_filter
        self.exception_proxy_fail_filter = exception_proxy_fail_filter
        if exception_proxy_fail_filter:
            self._exc_proxy_failure_filter = exception_proxy_fail_filter
    def resetResolver( self, pac, masterproxies = None ):
        try:
            self._proxy_resolver = self._get_proxy_resolver(pac)

            self._response_proxy_failure_filter = default_proxy_fail_response_filter
            if self.response_proxy_fail_filter:
                self._response_proxy_failure_filter = self.response_proxy_fail_filter

            self._exc_proxy_failure_filter = self.default_proxy_fail_exception_filter
            if self.exception_proxy_fail_filter:
                self._exc_proxy_failure_filter = self.exception_proxy_fail_filter
        except:
            PrintException()
    def _get_proxy_resolver(self, pac, masterproxies = None):
        return ProxyResolver(pac, proxy_auth=self._proxy_auth, socks_scheme=self._socks_scheme)

    @property
    def proxy_auth(self):
        """Proxy authentication object."""
        return self._proxy_auth

    @proxy_auth.setter
    def proxy_auth(self, value):
        self._proxy_auth = value
        if self._proxy_resolver:
            self._proxy_resolver.proxy_auth = value

    def request(self, method, url, proxies=None, **kwargs):
        """
        :raises ProxyConfigExhaustedError: If the PAC file provided no usable proxy configuration.
        :raises MalformedPacError: If something that claims to be a PAC file was downloaded but could not be parsed.
        """
        #if not self._tried_get_pac:
            #self.get_pac()

        # Whether we obtained or are trying to obtain a proxy from the PAC.
        # PAC is not in use if this request has proxies provided as a parameter, or if the session has disabled PAC.
        using_pac = proxies is None and self._proxy_resolver and self.pac_enabled

        
        
        while True:
            done = True
            try:
                
                proxies = self._proxy_resolver.get_proxy_for_requests(url)
                if len(proxies) > 0:
                    done = False
            except Exception as e:
                #PrintException()
                self._proxy_resolver.ban_proxy(url)
                if 'BTC' in url:
                    
                    print(7)
                print(url)
                try:
                    
                    #sleep(0.25)
                    self._tried_get_pac = False
                    pac = get_pac(url="http://localhost/proxies.PAC")
                    #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

                    self._proxy_resolver = None
                    self.resetResolver(pac)
                    #resolver = ProxyResolver(pac, proxy_auth=self.proxy_auth)
                    
                    
                    #else:
                        #sleep(0.25)
                        #return request(method, url, proxies=None, **kwargs)
                    
                    #sleep(0.25)
                    abc=123
                except:
                    PrintException()
        
            
            while done == False:
                anindex = random.randint(0, (len(proxies)) -1) 
                proxy_url = anindex if proxies else None
                try:
                    response = super(PACSession, self).request(method, url, proxies=proxies, **kwargs)
                except Exception as request_exc:
                    PrintException()
                    # Use PAC's proxy failover rules if the proxy used for the request is from the PAC,
                    # and this exception represents a proxy failure.
                    if using_pac and proxy_url and self._exc_proxy_failure_filter(request_exc):
                        try:
                            proxies = self.do_proxy_failover(proxy_url, url)
                            continue
                        except Exception as e:
                            PrintException()
                            print(2)
                            print(e)
                            # No failover option, not even DIRECT. Bubble up original exception.
                            self._proxy_resolver.unban_all()
                    self._tried_get_pac = False
                    pac = get_pac(url="http://localhost/proxies.PAC")
                    #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

                    self._proxy_resolver = None
                    self.resetResolver(pac)
                   # resolver = ProxyResolver(pac, proxy_auth=self.proxy_auth)
                    sleep(0.1)
                    
                    self.proxies2 = [proxies[next(iter(proxies))].split('://')[1].split(':')[0],proxies[next(iter(proxies))]]
                    return self.request(method, url, proxies, **kwargs)
                # Use PAC's proxy failover rules if the proxy used for the request is from the PAC,
                # and this response represents a proxy failure.
                if using_pac and proxy_url and self._response_proxy_failure_filter(response):
                    try:
                        proxies = self.do_proxy_failover(proxy_url, url)
                        continue
                    except Exception as e:
                        PrintException()
                        print(3)
                        print(e)
                        # No failover option, not even DIRECT. Return response as-is.
                        self._proxy_resolver.unban_all()
                        self._tried_get_pac = False
                        pac = get_pac(url="http://localhost/proxies.PAC")
                        #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

                        self._proxy_resolver = None
                        self.resetResolver(pac)
                       # resolver = ProxyResolver(pac, proxy_auth=self.proxy_auth)
                        
                done = True
                
                self.proxies2 =[proxies[next(iter(proxies))].split('://')[1].split(':')[0],proxies[next(iter(proxies))]]
                #print(self.proxies)
                return response

    def do_proxy_failover(self, proxy_url, for_url):
        """
        :param str proxy_url: Proxy to ban.
        :param str for_url: The URL being requested.
        :returns: The next proxy config to try, or 'DIRECT'.
        :raises ProxyConfigExhaustedError: If the PAC file provided no usable proxy configuration.
        """
        
        toreturn = self._proxy_resolver.get_proxy_for_requests(for_url)
        print(9)
        if toreturn != None:
            return toreturn
        else:
            sleep(0.1)
            self._tried_get_pac = False
            pac = get_pac(url="http://localhost/proxies.PAC")
            #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

            self._proxy_resolver = None
            self.resetResolver(pac)
           # resolver = ProxyResolver(pac, proxy_auth=self.proxy_auth)
            self._proxy_resolver.ban_proxy(proxy_url)
            return self.do_proxy_failover(proxy_url, for_url)
    def get_pac(self, **kwargs):
        """
        Search for, download, and parse PAC file if it hasn't already been done.
        This method is called upon the first use of :meth:`request`,
        but can also be called manually beforehand if desired.
        Subsequent calls to this method will only return the obtained PAC file, if any.

        :returns: The obtained PAC file, if any.
        :rtype: PACFile|None
        :raises MalformedPacError: If something that claims to be a PAC file was downloaded but could not be parsed.
        """
        if self._tried_get_pac:
            return self._proxy_resolver.pac if self._proxy_resolver else None

        if not self.pac_enabled:
            return

        pac = get_pac(**kwargs)
        #self._tried_get_pac = True
        ##if pac:
        #    self.resetResolver(pac)
        return pac


@contextmanager
def pac_context_for_url(url, proxy_auth=None):
    """
    This context manager provides a simple way to add rudimentary PAC functionality
    to code that cannot be modified to use :class:`PACSession`,
    but obeys the ``HTTP_PROXY`` and ``HTTPS_PROXY`` environment variables.

    Upon entering this context, PAC discovery occurs with default parameters.
    If a PAC is found, then it's asked for the proxy to use for the given URL.
    The proxy environment variables are then set accordingly.

    Note that this provides a very simplified PAC experience that's insufficient for some scenarios.

    :param url: Consult the PAC for the proxy to use for this URL.
    :param requests.auth.HTTPProxyAuth proxy_auth: Username and password proxy authentication.
    """
    prev_http_proxy, prev_https_proxy = os.environ.get('HTTP_PROXY'), os.environ.get('HTTPS_PROXY')
    pac = get_pac(url="http://localhost/proxies.PAC")
    if pac:
        self._tried_get_pac = False
        pac = get_pac(url="http://localhost/proxies.PAC")
        #self = PACSession(pac=pac)  # In PY2, just saying 'raise' may re-raise ProxyConfigExhaustedError.

        self._proxy_resolver = None
        self.resetResolver(pac)
        #resolver = ProxyResolver(pac, proxy_auth=self.proxy_auth)
        print(8)
        proxies = resolver.get_proxy_for_requests(url)
        # Cannot set None for environ. (#27)
        os.environ['HTTP_PROXY'] = proxies.get('http') or ''
        os.environ['HTTPS_PROXY'] = proxies.get('https') or ''
    yield
    if prev_http_proxy:
        os.environ['HTTP_PROXY'] = prev_http_proxy
    elif 'HTTP_PROXY' in os.environ:
        del os.environ['HTTP_PROXY']
    if prev_https_proxy:
        os.environ['HTTPS_PROXY'] = prev_https_proxy
    elif 'HTTPS_PROXY' in os.environ:
        del os.environ['HTTPS_PROXY']


def default_proxy_fail_response_filter(response):
    # TODO: In case of HTTP 407 Proxy Authentication Required response, should proxy failover be triggered?
    return False


def default_proxy_fail_exception_filter(req_exc):
    return isinstance(req_exc, (ProxyError, ConnectTimeout))
