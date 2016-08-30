import asyncio

from api_handler import ApiHandler

class ServiceRouter:
    api_dict = dict()

    def register_api(self, api, handler):
        if False == (handler is ApiHandler):
            assert('Invalid Api Handler %s|%s' % (api, handler))
        temp = self.api_dict.get(api, None)
        if temp is None:
            self.api_dict[api] = handler
        else:
            assert('Dupilicate Api %s: %s | %s' % (api, temp, handler))

    async def async_call_api(api, args, context):
        try:
            handler = api_router_dic.get(api, None)
            if handler is None:
                # todo discovery remote service
                return None, 'Invalid API {}'.format(api)

            return handler.process(args, context)
        except Exception as e:
            print('call_api_error %s:%s,%s,%s' % (e, api, args, context))
            return None, 'Internal_Error'