import asyncio
from aiohttp import web

async def hello(request):
    print(request.path)
    return web.Response(body=b"Hello, world")

app = web.Application()
app.router.add_route('*', '/', hello)
web.run_app(app)