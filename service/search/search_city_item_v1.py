import functools

import rule
import router
import util
import environment as env
import util.elasticsearch as es

from .common import consts, item_helper

class SearchCityItemV1(router.ApiHandler):
    def __init__(self):
        self._index = 'fivemiles'
        self._doc_type = 'item'


    async def process(self, args, context=None):
        offset = args.get('offset')
        size = args.get('size')
        lat = args.get('lat')
        lon = args.get('lon')

        now = util.get_timestamp()

        query = es.dsl.Filtered().must([
            es.dsl.Range('updated_at', dict(gt=now/1000 - consts.ITEM_EXPIRE_DURATION)),
            es.dsl.Term('@is_removed', 0),
            es.dsl.Range('weight', dict(gt=0)),
            es.dsl.Term('owner.state', 1)
        ]).must_not(
            es.dsl.Term('owner.is_robot', 1)            
        )

        query.must(item_helper.city_filter(args))
        query.must(item_helper.root_category_filter(args))
        query.must(item_helper.category_filter(args))
        query.must(item_helper.price_range_filter(args))

        if args.get('diamond') == 0:
            query.must(es.dsl.Term('diamond_enabled', 0))
        else:
            query.must(item_helper.trade_type_filter(args))
        
        es_query = es.dsl.FunctionScore().query(query)

        body = es.ESSearchBody(
            es_query
        ).page_range(
            from_index=offset, size=size
        ).aggregation(
            'group_by_cat_id', es.aggr.Terms('cat_id', 100)
        )

        orderby = args.get('orderby')
        if orderby == 1:
            body.orderby('created_at', order='desc').orderby_score()
        elif orderby == 2:
            body.orderby_distance('location_2', "%s, %s" % (lat, lon), order='asc').orderby_score()            
        elif orderby == 3:
            body.orderby('price', order='asc').orderby_score()
        elif orderby == 4:
            body.orderby('price', order='desc').orderby_score()
        else:
            es_query.decay(
                name='gauss', 
                field='listing_at', 
                origin=now/1000, 
                offset=0, 
                scale=consts.GAUSS_DATE_SCALE, 
                decay=0.5
            ).decay(
                name='gauss', 
                field='location_2', 
                origin='%s,%s'%(lat, lon), 
                decay=0.22, 
                scale='%smi'%(consts.GAUSS_DISTANCE_SCALE), 
                offset='%smi'%(consts.GAUSS_DISTANCE_OFFSET)
            )


        es_result, err = await es.search(
            host = env.hosts.get_item_es_host(),
            index = self._index,
            doc_type = self._doc_type,
            body = body
        )          

        if err is not None:
            return None, err
        
        result = dict(
            total=es_result.get('total',0),
            objects= es_result.get('hits', []),
        )

        for item in result['objects']:
            item_helper.format_item_local_price(item)

        aggs = es_result.get('aggs', None)
        if aggs is not None:
            group_by_cat_id = aggs.get('group_by_cat_id', None)
            if group_by_cat_id is not None:
                categorys = []
                buckets = group_by_cat_id.get('buckets', [])
                for item in buckets:
                    categorys.append(dict(id=item['key'], cnt=item['doc_count']))    
                result['refind_category'] = categorys
        return result, None


router.register_api_handler(
    '/api/search/city/item/v1',
    SearchCityItemV1(), 
    rule_func = functools.partial(rule.and_rule, dict(
        rules=[
            functools.partial(rule.check_params_rule, [('city', str)]),
            functools.partial(rule.check_option_params_rule, [
                ('root_cat_id', int, -2),
                ('cat_id', int, -2),
                ('offset', int, 0),
                ('size', int, 30), 
                ('lat', float, 0.0),
                ('lon', float, 0.0),
                ('distance', int, None),
                ('diamond', int, 1),
                ('trade_type', int, 0),
                ('area', int, 0),
                ('orderby', int, 0),
                ('min_price', float, None),
                ('max_price', float, None),
                ]),
        ]
)))
