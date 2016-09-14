import asyncio
import aiohttp

from aiohttp.resolver import AsyncResolver

async def async_http(method, url, headers = dict(), body = None):
    resolver = AsyncResolver(nameservers=['8.8.8.8', '8.8.4.4'])
    with aiohttp.ClientSession(
        connector = aiohttp.TCPConnector(limit = 32, resolver = resolver),
        loop = asyncio.get_event_loop()) as session:
        try:
            with aiohttp.Timeout(5):
                async with session.request(
                    method = method,
                    url = url, 
                    headers = headers,
                    data = body) as resp:
                    raw = await resp.content.read()
                    return  (resp.status, resp.headers, raw), None
        except aiohttp.errors.TimeoutError:
            return None, 'Timeout'
        except Exception as e:
            return None, e

