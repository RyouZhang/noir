import asyncio
from urllib.parse import urlparse, parse_qsl

import aiohttp
import aiohttp.server
from aiohttp import MultiDict


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
  async def handle_request(self, message, payload):
      response = aiohttp.Response(
          self.writer, 200, http_version=message.version
      )
      print(self, message, payload)
      response.add_header('Content-Type', 'text/html')
      response.add_header('Content-Length', '18')
      response.send_headers()
      response.write(b'<h1>It Works!</h1>')
      await response.write_eof()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    f = loop.create_server(
        lambda: HttpRequestHandler(debug=True, keep_alive=75),
        '0.0.0.0', '8080')
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass