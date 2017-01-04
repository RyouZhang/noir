import time
import functools

import rule
import router
import environment as env
import util.http as http
import util.elasticsearch as es
import util.json as json

# input params
# id, user_id
class NewsOpenV1(router.ApiHandler):

    def __init__(self):
        self._index = 'fivemiles_news'
        self._doc_type = 'news'


    async def process(self, args, context = None):  

        result, err = await es.update_one(
            host = env.hosts.get_news_es_host(),
            index = self._index,
            doc_type = self._doc_type,
            id = args['id'], 
            body = dict(
                fields = ['pv', 'link', 'fake_pv'],
                script = dict(lang = 'painless', file = 'update_pv'))
        )

        if err is not None:
            return None, err
        
        result['id'] = args['id']
        if result.get('fake_pv', None) is not None:
            result['pv'] = result['pv'] + result['fake_pv'] + 1
            del result['fake_pv']
        
        return result, None     

router.register_api_handler(
    '/api/news/open/v1', 
    NewsOpenV1(),
    rule_func = functools.partial(rule.check_params_rule, [('id', str)]))