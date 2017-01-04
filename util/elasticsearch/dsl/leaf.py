from .base import *

__all__ = (
    'Term',
    'Terms',
    'Range',
    'Exists',
    'Wildcard',
    'Regexp',
    'Ids',
    'Match',
    'MultiMatch',
    'Script',
    'ScriptScore',
    'GeoDistance',
    'GeoDistanceRange',
    'GeoBoundingBox',
)


class Term(ESLeafClause):

    def __init__(self, key, value, ext=dict()):
        super(Term, self).__init__()
        self['term'] = dict()
        self['term'][key] = dict(value=value, **ext)

class Terms(ESLeafClause):

    def __init__(self, key, values):
        super(Terms, self).__init__()
        self['terms'] = dict()
        self['terms'][key] = values

class Range(ESLeafClause):

    def __init__(self, key, value):
        super(Range, self).__init__()
        self['range'] = dict()
        self['range'][key] = dict(**value)

class Exists(ESLeafClause):

    def __init__(self, key, value):
        super(Exists, self).__init__()
        self['exists'] = dict()
        self['exists'][key] = value

class Prefix(ESLeafClause):

    def __init__(self, key, value, ext=dict()):
        super(Prefix, self).__init__()
        self['prefix'] = dict()
        self['prefix'][key] = dict(value=value, **ext)

class Wildcard(ESLeafClause):

    def __init__(self, key, value, ext=dict()):
        super(Wildcard, self).__init__()
        self['wildcard'] = dict()
        self['wildcard'][key] = dict(value=value, **ext)

class Regexp(ESLeafClause):

    def __init__(self, key, value, ext=dict()):
        super(Regexp, self).__init__()
        self['regexp'] = dict()
        self['regexp'][key] = dict(value=value, **ext)        

class Ids(ESLeafClause):

    def __init__(self, values, doc_type=None):
        super(Ids, self).__init__()
        self['ids'] = dict(values=values, type=doc_type)



class Match(ESLeafClause):

    def __init__(self, key, value, ext=dict()):
        super(Match, self).__init__()
        self['match'] = dict(key = value, **ext)


class MultiMatch(ESLeafClause):
    def __init__(self, keys, value, match_type='best_fields',ext=dict()):
        super(MultiMatch, self).__init__()
        self['multi_match'] = dict(query=value, fields=keys, type=match_type, **ext)


class Script(ESLeafClause):
    def __init__(self, lang='painless', script=None, file=None, params=dict()):
        assert(lang == 'native' or lang == 'painless')
        if script is not None:
            self['script'] = dict(script=dict(lang=lang, script=script, params=params))
        elif file is not None:
            self['script'] = dict(script=dict(lang=lang, file=file, params=params))
        else:
            assert(False)


class ScriptScore(ESLeafClause):
    def __init__(self, script, lang='painless', params=dict()):
        assert(lang == 'native' or lang == 'painless')
        self['script_score'] = dict(script=dict(lang=lang, inline=script, params=params))


class GeoDistance(ESLeafClause):
    def __init__(self, key, distance='5km'):
        super(GeoDistance, self).__init__()
        self._key = key
        self['geo_distance'] = dict(distance=distance)
    
    def center_poi(self, lat, lon):
        self['geo_distance'][self._key] = dict(lat=lat, lon=lon)
        return self
    
    def center_hash(self, hash_code):
        self['geo_distance'][self._key] = hash_code
        return self


class GeoDistanceRange(ESLeafClause):
    def __init__(self, key, from_distance='0km', to_distance='50km'):
        super(GeoDistance, self).__init__()
        self._key = key
        self['geo_distance_range'] = {'from':from_distance, 'to':to_distance}
    
    def center_poi(self, lat, lon):
        self['geo_distance'][self._key] = dict(lat=lat, lon=lon)
        return self
    
    def center_hash(self, hash_code):
        self['geo_distance'][self._key] = hash_code
        return self



class GeoBoundingBox(ESLeafClause):
    def __init__(self, key):
        super(GeoBoundingBox, self).__init__()
        self._key = key
        self['geo_bounding_box'] = dict()
        self['geo_bounding_box'][self._key] = dict()
    
    def bottom_right_poi(self, lat, lon):
        loc = self['geo_bounding_box'][self._key]
        loc['bottom_right'] = dict(lat=lat, lon=lon)
        return self

    def top_left_poi(self, lat, lon):
        loc = self['geo_bounding_box'][self._key]
        loc['top_left'] = dict(lat=lat, lon=lon)        
        return self

    def bottom_right_hash(self, hash_code):
        loc = self['geo_bounding_box'][self._key]
        loc['top_left'] = hash_code            
        return self

    def top_left_hash(self, hash_code):
        loc = self['geo_bounding_box'][self._key]
        loc['top_left'] = hash_code           
        return self
