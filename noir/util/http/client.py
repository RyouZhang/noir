from urllib.parse import urlparse
import logging
import asyncio
import aiohttp

logger = logging.getLogger()

class HTTPClient(object):
    def __init__(self):
        self._lock = asyncio.Lock()
        self._session = None

    async def async_call(self, url, method='GET', headers=dict(), body=None, timeout=10):
        url_info = urlparse(url)
        if url_info is None:
            return (None, None, None), 'Invalid_URL'

        await self._lock.acquire()
        if self._session is None or self._session.closed is True:
            self._session = None
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    # conn_timeout=5,
                    keepalive_timeout=45,
                    limit=8),
                loop=asyncio.get_event_loop())
        self._lock.release()

        resp = None
        try:
            resp = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=body,
                    timeout=timeout)
            raw = await resp.content.read()
            await resp.release()
            return (resp.status, resp.headers, raw), None
        except asyncio.TimeoutError: 
            logger.error('http request timeout %s %s %s', method, url, body)
            if resp is not None:
                logger.error('http response timeout %s %s %s', resp.method, resp.status, resp.reason)
                resp.close()            
            return (None, None, None), 'Timeout'
        except Exception as e:
            logger.error('http request error %s %s %s', method, url, body)
            if resp is not None:
                resp.close()
            return (None, None, None), str(e)


client = HTTPClient()


async def async_request(url, method='GET', headers=dict(), body=None, raw_body_func=None, timeout=10):
    if body is None and raw_body_func is not None:
        body = await raw_body_func()
    result, err = await client.async_call(url, method=method, headers=headers, body=body, timeout=timeout)
    return result, err

