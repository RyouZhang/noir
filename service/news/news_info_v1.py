import functools

import rule
import router
import environment as env
import util.elasticsearch as es


class NewsInfoV1(router.ApiHandler):

    def __init__(self):
        self._index = 'fivemiles_news'
        self._doc_type = 'news'


    async def process(self, args, context=None):
        result, err = await es.mget(
            host=env.hosts.get_news_es_host(),
            index=self._index,
            doc_type=self._doc_type,
            ids=[args['id']],
            include_fields=args.get('fields', None),
            exclude_fields=['source_url'])            

        if err is not None:
            return None, err

        return result[args['id']], None


router.register_api_handler(
    '/api/news/info/v1',
    NewsInfoV1(),
    rule_func=functools.partial(rule.check_params_rule, [('id', str)]))
