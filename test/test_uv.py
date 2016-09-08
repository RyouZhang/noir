import signal

import pyuv

loop = pyuv.Loop.default_loop()

# def signal_cb(handle, signum):
#     signal_h.close()
#     # loop.stop()

# signal_h = pyuv.Signal(loop)
# signal_h.start(signal_cb, signal.SIGINT)

def close_handler(handler):
    print(handler.closed)

def callback(handler):
    print(handler)
    a.close(close_handler)

a = pyuv.Async(loop, callback)
print(a)
a.send()

loop.run()