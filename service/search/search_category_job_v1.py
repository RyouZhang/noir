import functools

import rule
import router
import util
import environment as env
import util.elasticsearch as es

from .common import consts, item_helper, distance_helper
from .search_api_handler import SearchApiHandler


class SearchCategoryJobV1(SearchApiHandler):
    
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
            es.dsl.Term('owner.state', 1),
        ]).must_not(
            es.dsl.Term('owner.is_robot', 1)            
        )

        query.must(item_helper.root_category_filter(args))
        query.must(item_helper.category_filter(args))

        if args.get('diamond') == 0:
            query.must(es.dsl.Term('diamond_enabled', 0))
        else:
            query.must(item_helper.trade_type_filter(args))
        
        query.must(item_helper.price_range_filter(args))

        distance = args.get('distance')
        if distance is not None:
            (tl_lat, tl_lon), (br_lat, br_lon) = distance_helper.generate_geo_box(lat, lon, distance, is_km=False)
    
            query.should(
                es.dsl.GeoBoundingBox('location_2').top_left_poi(tl_lat, tl_lon).bottom_right_poi(br_lat, br_lon)
            )

            if args.get('area') == 2:
                query.should(
                    es.dsl.Bool().must([
                        es.dsl.Term('diamond_enabled', 1),
                        es.dsl.Terms('shipping_method', [2, 3])  
                    ]).must_not(
                        es.dsl.GeoBoundingBox('location_2').top_left_poi(tl_lat, tl_lon).bottom_right_poi(br_lat, br_lon)
                    )
                )
        
        es_query = es.dsl.FunctionScore().query(query).decay(
            name='gauss', field='weight', origin=10, scale=3, offset=5, decay=0.2
        )

        body = es.ESSearchBody(
            es_query
        ).page_range(
            from_index=offset, size=size
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
                name='gauss', field='listing_at', origin=now/1000, offset=0, scale=consts.GAUSS_DATE_SCALE, decay=0.5
            ).decay(
                name='gauss', field='location_2', origin='%s,%s'%(lat, lon), decay=0.22,
                scale='%smi' % consts.GAUSS_DISTANCE_SCALE, offset='%smi' % consts.GAUSS_DISTANCE_OFFSET
            )

        # if util.is_not_production():
        util.logger.info("es_search_exec=%s" % ("%s" % body).replace("'", "\""))

        util.logger.info('es_search_body %s', body)

        es_result, err = await es.search(
            host=env.hosts.get_item_es_host(),
            index=self._index,
            doc_type=self._doc_type,
            body=body
        )          

        if err is not None:
            return None, err
        
        result = dict(
            total=es_result.get('total',0),
            objects=es_result.get('hits', []),
        )

        for item in result['objects']:
            item_helper.format_item_local_price(item)

        return result, None


router.register_api_handler(
    '/api/search/category/job/v1',
    SearchCategoryJobV1(), 
    rule_func=functools.partial(rule.and_rule, dict(
        rules=[
            functools.partial(rule.check_params_rule, [('root_cat_id', int)]),
            functools.partial(rule.check_option_params_rule, [
                ('cat_id', int, -2),
                ('offset', int, 0),
                ('size', int, 30), 
                ('lat', float, 0.0),
                ('lon', float, 0.0),
                ('country', str, None),
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