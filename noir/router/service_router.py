# -*- coding: utf-8 -*-

import types
import logging
import asyncio
import functools

import noir.util as util
from noir.router.service_handler import ServiceHandler
from noir.router.service_rewrite import service_rewrite

logger = logging.getLogger()

__all__ = [
    'register_service_handler',
]


def register_service_handler(path, handler, rule_func=None):
    service_router._register_service(path, handler, rule_func)

class ServiceRouter:
    
    def __init__(self):
        self._router_dic = dict()


    def _register_service(self, path, handler, rule_func):
        if False == handler is ServiceHandler:
            assert('Invalid Service Handler %s|%s' % (path, handler))

        temp = self._router_dic.get(path, None)
        if temp is None:
            self._router_dic[path] = (rule_func, handler)
        else:
            assert('Dupilicate Service %s: %s | %s' % (path, temp, handler))
        
        logger.info('Register Service %s Handler %s', path, handler)


    async def async_call_api(self, path, args, context, timeout=None):
        try:
            path, args, context = await service_rewrite.async_rewrite_service(path, args, context)

            (rule_func, handler) = self._router_dic.get(path, (None, None))
            if handler is None:
                # todo discovery remote service
                logger.warning('invalid_service %s,%s,%s', path, args, context)
                return None, 'Invalid Service {}'.format(path)

            if rule_func is not None:
                result, err = await rule_func(args, context)
                if err is not None:
                    return None, err
  
            async_task = asyncio.ensure_future(handler.process(args, context), loop=asyncio.get_event_loop())
            try:
                (res, err) = await asyncio.wait_for(async_task, timeout)
                if err is not None:
                    logger.error('call_api_error %s,%s,%s,%s', err, path, args, context)
                return res, err
            except asyncio.TimeoutError:
                if async_task is not None and not async_task.cancelled():
                    async_task.cancel()                
                return None, 'Time_out'

        except Exception as e:
            logger.error('call service exception %s,%s,%s,%s', e, path, args, context)
            return None, 'Internal_Error'


service_router = ServiceRouter()
