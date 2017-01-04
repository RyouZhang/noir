# -*- coding: utf-8 -*-

import types
import asyncio
import functools

import util
from router.api_handler import ApiHandler


MAX_RWERITE_DEEP = 3


def register_api_handler(api, handler, rule_func=None):
    service_router.register_api(api, handler, rule_func)


# rewrite_func(api, args, context) -> api, args, context
def register_api_rewrite(api, rewrite_func):
    service_router.register_rewrite(api, rewrite_func)


class ServiceRouter:
    
    def __init__(self, max_rewrite_deep=MAX_RWERITE_DEEP):
        self._api_router_dic = dict()
        self._api_rewrite_dic = dict()
        self._max_rewrite_deep = MAX_RWERITE_DEEP


    def register_api(self, api, handler, rule_func):
        if False == handler is ApiHandler:
            assert('Invalid Api Handler %s|%s' % (api, handler))
        temp = self._api_router_dic.get(api, None)
        if temp is None:
            self._api_router_dic[api] = (rule_func, handler)
        else:
            assert('Dupilicate Api %s: %s | %s' % (api, temp, handler))
        
        util.logger.info('register api %s handler %s', api, handler)


    def register_rewrite(self, api, rewrite_func):
        if isinstance(rewrite_func, types.FunctionType):
            target = self._api_rewrite_dic.get(api, None)
            if target is None:
                self._api_rewrite_dic[api] = rewrite_func
            else:
                assert('Dupilicate Rewrite Api %s: %s | %s' % (api, temp, handler))


    async def async_rewrite_api(self, api, args, context, rewrite_deep=0):
        rewrite_func = self._api_rewrite_dic.get(api, None)
        if rewrite_func is not None:
            rw_api, args, context = await rewrite_func(api, args, context)
        
            if rw_api is api:
                return rw_api, args, context
            
            if rewrite_deep + 1 >= self._max_rewrite_deep:
                util.logger.warning('rewrite_api_max_times %s to %s', api, rw_api)
                return rw_api, args, context
            
            return await self.async_rewrite_api(rw_api, args, context, rewrite_deep=rewrite_deep+1)   
        
        return api, args, context


    async def async_call_api(self, api, args, context, timeout=None):
        try:
            api, args, context = await self.async_rewrite_api(api, args, context)

            (rule_func, handler) = self._api_router_dic.get(api, (None, None))
            if handler is None:
                # todo discovery remote service
                util.logger.warning('invalid_api %s,%s,%s', api, args, context, exc_info=True)
                return None, 'Invalid API {}'.format(api)

            if rule_func is not None:
                result, err = await rule_func(args, context)
                if err is not None:
                    util.logger.warning('call_api_rule_error %s,%s,%s,%s', err, api, args, context, exc_info=True)
                    return None, err
  
            async_task = asyncio.ensure_future(handler.process(args, context), loop=asyncio.get_event_loop())
            try:
                (res, err) = await asyncio.wait_for(async_task, timeout, loop=asyncio.get_event_loop())
                if err is not None:
                    util.logger.error('call_api_error %s,%s,%s,%s', err, api, args, context, exc_info=True)
                return res, err
            except asyncio.TimeoutError:
                if async_task is not None and not async_task.cancelled():
                    async_task.cancel()                
                return None, 'Time_out'

        except Exception as e:
            util.logger.error('call_api_exception %s,%s,%s,%s', e, api, args, context, exc_info=True)
            return None, 'Internal_Error'

service_router = ServiceRouter()
