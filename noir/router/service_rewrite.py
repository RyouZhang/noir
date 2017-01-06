import types
import asyncio
import functools

__all__ = [
    'register_service_rewrite'
]

# rewrite_func(api, args, context) -> api, args, context
def register_service_rewrite(path, rewrite_func):
    service_rewrite._register_rewrite(path, rewrite_func)

MAX_RWERITE_DEEP = 3

class ServiceRewrite:

    def __init__(self, max_rewrite_deep=MAX_RWERITE_DEEP):
        self._max_rewrite_deep = max_rewrite_deep
        self._rewrite_dic = dict()

    def _register_rewrite(self, path, rewrite_func):
        if isinstance(rewrite_func, types.FunctionType):
            target = self._rewrite_dic.get(path, None)
            if target is None:
                self._rewrite_dic[path] = rewrite_func
            else:
                assert('Dupilicate Rewrite Service Path %s: %s | %s' % (path, rewrite_func, target))


    async def async_rewrite_service(self, path, args, context, rewrite_deep=0):
        rewrite_func = self._rewrite_dic.get(path, None)
        if rewrite_func is not None:
            rw_path, args, context = await rewrite_func(path, args, context)
        
            if rw_path is path:
                return rw_path, args, context
            
            if rewrite_deep + 1 >= self._max_rewrite_deep:
                util.logger.warning('Rewrite Service Max Times %s to %s', path, rw_path)
                return rw_path, args, context
            
            return await self.async_rewrite_service(rw_path, args, context, rewrite_deep=rewrite_deep+1)   
        
        return path, args, context


service_rewrite = ServiceRewrite()