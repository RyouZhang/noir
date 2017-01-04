
import router


class SearchApiHandler(router.ApiHandler):

    async def process(self, args, context=None):
        return None, 'Invalid_Request' 

    def build_search_query(self, args):
        return None

    def build_search_body(self, args):
        return None