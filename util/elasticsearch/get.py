import functools
from urllib.parse import urljoin, urlencode

import util.json as json
import util.http as http
import util

__all__ = (
    'get_one'
)

async def get_one(host, index, doc_type, id, include_fields = None, exclude_fields = None):
    url = build_get_url(host, index, doc_type, id, include_fields, exclude_fields)
    if url is None:
        return None, 'Invalid_Params'
    
    (status, headers, raw), err = await http.async_request(url)
    if err is not None:
        return None, err

    result, err = parse_get_result(status, headers, raw)
    if err is not None:
        return None, err

    result['id'] = id
    return result, None


def build_get_url(host, index, doc_type, id, include_fields = None, exclude_fields = None):
    if any(x is None for x in (host, index, doc_type, id)):
        return None

    params = dict()
    if exclude_fields is not None:
        params['_source_exclude'] = ','.join(exclude_fields)
    if include_fields is not None:
        params['_source_include'] = ','.join(include_fields)

    return urljoin(host, '%s/%s/%s/_source?%s' % (index, doc_type, id, urlencode(params)))


def parse_get_result(status, headers, raw):
    if status != 200:
        return None, 'Request_Failed'
    try:
        result = json.convert_from_json_raw(raw)
        return result, None
    except Exception as e:
        return None, 'Invalid_Result'