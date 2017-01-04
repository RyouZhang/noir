import json

async def async_convert_to_json_raw(obj, encode = 'UTF-8'):
    return convert_to_json_raw(obj, encode)

def convert_to_json_raw(obj, encode = 'UTF-8'):
    return json.dumps(obj).encode(encode)

async def async_convert_from_json_raw(raw, encode = 'UTF-8'):
    return convert_from_json_raw(raw, encode)

def convert_from_json_raw(raw, encode = 'UTF-8'):
    return json.loads(raw.decode(encode))
