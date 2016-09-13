import os
import asyncio

import router
import rule
import service
import entry

if __name__ == '__main__':
    port = os.getenv('SERVER_PORT', '8080')

    loop = asyncio.get_event_loop()
    f = loop.create_server(
        lambda: entry.HttpRequestHandler(debug=False, keep_alive=90),
        '0.0.0.0', port)
    
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass