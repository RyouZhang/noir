import asyncio
import functools

from router.api_handler import ApiHandler

def register_api_handler(api, handler):
    serviceRouter.register_api(api, handler)

class ServiceRouter:
    api_router_dic = dict()

    def register_api(self, api, handler):
        if False == (handler is ApiHandler):
            assert('Invalid Api Handler %s|%s' % (api, handler))
        temp = self.api_router_dic.get(api, None)
        if temp is None:
            self.api_router_dic[api] = handler
        else:
            assert('Dupilicate Api %s: %s | %s' % (api, temp, handler))

    async def async_call_api(self, api, args, context, timeout = None):
        try:
            handler = self.api_router_dic.get(api, None)
            if handler is None:
                # todo discovery remote service
                return None, 'Invalid API {}'.format(api)

            async_task = asyncio.ensure_future(handler.process(args, context), loop = asyncio.get_event_loop())
            try:
                (res, err) = await asyncio.wait_for(async_task, timeout, loop = asyncio.get_event_loop())
                return res, err
            except asyncio.TimeoutError:
                async_task.cancel()
                return None, 'Time_out'
        except Exception as e:
            print('call_api_error %s:%s,%s,%s' % (e, api, args, context))
            return None, 'Internal_Error'

serviceRouter = ServiceRouter()