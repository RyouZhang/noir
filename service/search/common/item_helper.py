import util.elasticsearch as es


def format_item_local_price(item):
    if item.get('price', None) is not None:
        if item['price'] == 0.0:
            item['local_price'] = "Free"
        else:
            item['local_price'] = item['local_price'][:-3] + item['local_price'][-3:].replace('.00', '')


def root_category_filter(args):
    if args.get('root_cat_id') >= 0:
        return es.dsl.Term('root_cat_id', args.get('root_cat_id'))
    return None


def category_filter(args):
    if args.get('cat_id') >= 0:
        return es.dsl.Term('cat_id', args.get('cat_id'))
    return None


def price_range_filter(args):
    min_price = args.get('min_price')
    max_price = args.get('max_price')

    if min_price is not None or max_price is not None:
        temp = dict()
        if min_price is not None:
            temp['gte'] = min_price
        if max_price is not None:
            temp['lte'] = max_price
        return es.dsl.Range('price', temp)
    else:
        return None


def city_filter(args):
    if len(args.get('city')) >= 0:
        return es.dsl.Term('city', args.get('city').lower())
    return None

# trade_type
TRADE_TYPE_ALL              = 0
TRADE_TYPE_SHIPPING         = 1
TRADE_TYPE_LOCAL            = 2
TRADE_TYPE_SHIPPING_LOCAL   = 3


def trade_type_filter(args):
    trade_type = args.get('trade_type')

    if trade_type == TRADE_TYPE_ALL:
        return None
    if trade_type == TRADE_TYPE_SHIPPING:
        return [
            es.dsl.Term('diamond_enabled', 1),
            es.dsl.Terms('shipping_method', [2, 3])
        ]
    if trade_type == TRADE_TYPE_LOCAL:
        return [
            es.dsl.Term('diamond_enabled', 1),
            es.dsl.Terms('shipping_method', [1, 3])
        ]
    if trade_type == TRADE_TYPE_SHIPPING_LOCAL:
        return es.dsl.Term('diamond_enabled', 1)
    return None


def shipping_filter(args):
    if args.get('shipping_only') == 1:
        return [
            es.dsl.Term('diamond_enabled', 1),
            es.dsl.Terms('shipping_method', [2, 3])
        ]
    return None
