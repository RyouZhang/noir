import asyncio
import aiohttp

async def async_http(method, url, headers = dict(), body = None):
    with aiohttp.ClientSession() as session:
        try:
            with aiohttp.Timeout(5):
                async with session.request(
                    method = method,
                    url = url, 
                    headers = headers,
                    data = body) as resp:
                    return resp, None
        except aiohttp.errors.TimeoutError:
            return None, 'Timeout'
        except Exception as e:
            return None, e

