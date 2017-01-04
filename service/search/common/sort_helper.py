__all__ = (
    'get_sort_config'
)


sort_confs = {
    1:dict(field='location_2', order='asc'),
    2:dict(field='created_at', order='desc'),
    3:dict(field='price', order='asc'),
    4:dict(field='price', order='desc'),
}

def get_sort_config(key):
    return sort_confs.get(key, None)