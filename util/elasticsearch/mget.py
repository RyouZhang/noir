import functools
from urllib.parse import urljoin, urlencode

import util.json as json
import util.http as http
import util

__all__ = (
    'mget'
)

async def mget(host, index, doc_type, ids, include_fields = None, exclude_fields = None):
    if ids is None or len(ids) <= 0:
        return None, 'Invalid_Params'
    
    if any(x is None for x in (host, index, doc_type)):
        return None, 'Invalid_Params'

    params = dict()
    if exclude_fields is not None:
        params['_source_exclude'] = ','.join(exclude_fields)
    if include_fields is not None:
        params['_source_include'] = ','.join(include_fields)

    url = urljoin(host, '%s/%s/_mget?%s' % (index, doc_type, urlencode(params)))

    body = dict(ids = ids)

    (status, headers, raw), err = await http.async_request(url, 
        method = 'POST',
        headers = {"Transfer-Encoding":"identity"}, 
        raw_body_func = functools.partial(json.async_convert_to_json_raw, body))
    
    if err is not None:
        return None, err

    result, err = parse_mget_result(status, headers, raw)
    if err is not None:
        return None, err
    return result, None


def parse_mget_result(status, headers, raw):
    if status != 200:
        return None, 'Request_Failed'
    try:
        temp = json.convert_from_json_raw(raw)
        result = dict()
        for index in range(len(temp['docs'])):
            doc = temp['docs'][index]
            doc['_source']['id'] = doc['_id']
            result[doc['_id']] = doc['_source']

        return result, None
    except Exception as e:
        return None, 'Invalid_Result'