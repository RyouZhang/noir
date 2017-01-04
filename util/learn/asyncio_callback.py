# -*- coding: utf-8 -*-

import asyncio
import datetime

__author__ = 'lvyi'


@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(2)
    future.set_result('Future is done!')

def got_result(future):
    print("got_result=%s" % future.result())
    loop.stop()

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)
try:
    print("start")
    loop.run_forever()
finally:
    loop.close()
    print("end")
