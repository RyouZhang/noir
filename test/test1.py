import asyncio
import functools

async def test():
    await asyncio.sleep(10)
    print('asdasd')
    return 'hello'

def done_callback(future):
    print(future.result())

def main(loop):
    x = asyncio.run_coroutine_threadsafe(test(), loop)
    try:
        res = x.result(5)
    except asyncio.TimeoutError:
        print('fuck time out')
        x.cancel()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_at(loop.time() + 5, functools.partial(print, 'hello', flush=True))

    loop.call_soon(functools.partial(main, loop))

    asyncio.get_event_loop().run_forever()