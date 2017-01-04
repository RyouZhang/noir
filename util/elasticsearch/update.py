import functools
from urllib.parse import urljoin, urlencode

import util.json as json
import util.http as http
import util


__all__ = (
    'update_one'
)


async def update_one(host, index, doc_type, id, body, refresh = False):
    url = build_update_url(host, index, doc_type, id)
    if url is None:
        return None, 'Invalid_Params'

    (status, headers, raw), err = await http.async_request(url, 
        method = 'POST', 
        headers = {"Transfer-Encoding":"identity"}, 
        raw_body_func = functools.partial(json.async_convert_to_json_raw, body))
    if err is not None:
        return None, err

    result, err = parse_update_result(status, headers, raw)
    if err is not None:
        return None, err
    return result, None    


def build_update_url(host, index, doc_type, id):
    if any(x is None for x in (host, index, doc_type, id)):
        return None
    params = dict(
        retry_on_conflict = 5
    )
    return urljoin(host, '%s/%s/%s/_update?%s' % (index, doc_type, id, urlencode(params)))


def parse_update_result(status, headers, raw):
    if status != 200:
        return None, 'Request_Failed'
    try:
        result = json.convert_from_json_raw(raw)
        print(result)
        source = result.get('get', None)
        if source is None:
            return result, None
        else:
            if source.get('found', False) is False:
                return None, 'Invalid_Fields'
            result = dict()
            fields = source.get('fields', dict())
            for key in fields:
                values = fields.get(key, None)
                if values is not None:
                    result[key] = values[0]
            return result, None
    except Exception as e:
        return None, 'Invalid_Result'