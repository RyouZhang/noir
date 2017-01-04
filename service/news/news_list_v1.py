import math
import functools
from datetime import datetime

import rule
import router
import environment as env
import util.elasticsearch as es

import util
# input args
# user_id
# offset
class NewsListV1(router.ApiHandler):
    def __init__(self):
        self._index = 'fivemiles_news'
        self._doc_type = 'news'
        self._max_duration = 86400 * 90
        self._sort_script = "def weight=doc['weight'].value;if(weight==100){return Math.exp(params.deta * Math.abs(doc['published'].value*1000 - params.origin)/(51840000 * 9));}if(weight==99){return Math.exp(params.deta * Math.abs(doc['published'].value*1000 - params.origin)/(51840000 * 6));}if(weight==98||weight==97||weight==96||weight==95){return Math.exp(params.deta * Math.abs(doc['published'].value*1000 - params.origin)/(51840000));}return Math.exp(params.deta * Math.abs(doc['published'].value*1000 - params.origin)/(51840000));"
        
        # 'switch(_source["weight"]) {case [100]:return exp(deta * abs(doc["published"].value*1000 - origin)/(51840000 * 9))case [99]:return exp(deta * abs(doc["published"].value*1000 - origin)/(51840000 * 6))case [98, 97, 96, 95]:return exp(deta * abs(doc["published"].value*1000 - origin)/(51840000))default:return exp(deta * abs(doc["published"].value*1000 - origin)/(51840000))}'

    async def process(self, args, context):
        offset = args.get('offset')
        size = args.get('size')
        now = util.get_timestamp()

        body = es.ESSearchBody(
            es.dsl.FunctionScore(
                boost_mode='replace'
            ).query(                
                es.dsl.Bool().must(es.dsl.Range('published', dict(gte=now/1000.0 - self._max_duration)))
            ).script(
                es.dsl.ScriptScore(self._sort_script, lang='painless', params=dict(origin=now, deta=2*math.log(0.5)))
            )
        ).page_range(
            from_index=offset, size=size
        ).source_include(
            ['published', 'title', 'image', 'link', 'description', 'news_src', 'pv', 'fake_pv', 'weight']
        )

        es_result, err = await es.search(
            host = env.hosts.get_news_es_host(),
            index = self._index, 
            doc_type = self._doc_type,
            body = body)

        if err is not None:
            return None, err

        meta = dict(offset=offset, size=size)
        meta['total'] = es_result.get('total', 0)

        for news in es_result['hits']:
            news['pv'] = news.get('pv', 0) + news.get('fake_pv', 0)
            date_detail = datetime.fromtimestamp(news['published'])
            news['date_formart'] = '%s-%s-%s %s:%s:%s' % (date_detail.year, date_detail.month, date_detail.day, date_detail.hour, date_detail.minute, date_detail.second)
            if hasattr(news, 'fake_pv'):
                del news['fake_pv']
        
        if len(es_result['hits']) < size or offset + len(es_result['hits']) == meta['total']:
            meta['has_next'] = False
        else:
            meta['had_next'] = True

        result = dict(
            meta=meta,
            objects=es_result.get('hits', []),
        )

        return result, None

router.register_api_handler(
    '/api/news/list/v1', 
    NewsListV1(),
    rule_func = functools.partial(rule.check_option_params_rule, [('offset', int, 0), ('size', int, 30)]))