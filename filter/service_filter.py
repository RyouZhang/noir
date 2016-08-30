import asyncio

def register_api_filter(api, filters = None):
    if filters is None:
        return
    print(filters)
    [serviceFilter.register_filter(api, filter_func) for filter_func in filters]

class ServiceFilter:
    api_filter_dic = dict()

    def register_filter(self, api, filter_func):
        if filter_func is None:
            return
        filters = self.api_filter_dic.get(api, [])
        filters.append(filter_func)
        self.api_filter_dic[api] = filters
    
    async def check_api_filter(self, api, params, context):
        filters = self.api_filter_dic.get(api, [])
        for filter_func in filters:
            result, err = filter_func(params, context)
            if err is not None:
                return False, err
        return True, None

serviceFilter = ServiceFilter()