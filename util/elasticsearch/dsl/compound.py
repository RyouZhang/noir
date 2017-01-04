from .base import *


__all__ = (
    'Bool',
    'Filtered',
    'FunctionScore',
)

# ES2.0+ not support
class Filtered(ESCompoundClause):
    
    def __init__(self):
        super(Filtered, self).__init__()
        self._and = []
        self['filtered'] = {'filter':{'and':{'filters':self._and}}}
        self._not = None
        self._or = None

    def must(self, leafClause):
        if leafClause is None:
            return self

        if isinstance(leafClause, list):
            [self._and.append(x) for x in leafClause]
        else:
            self._and.append(leafClause)
        return self

    def must_not(self, leafClause):
        if leafClause is None:
            return self

        if self._not is None:
            self._not = []
            self._and.append({'not': {'and':self._not}})

        if isinstance(leafClause, list):
            [self._not.append(x) for x in leafClause]
        else:
            self._not.append(leafClause)
        return self

    def should(self, leafClause, minimum_match = 1):
        if leafClause is None:
            return self
        
        if self._or is None:
            self._or = []
            self._and.append({'or':self._or})

        if isinstance(leafClause, list):
            [self._or.append(x) for x in leafClause]
        else:
            self._or.append(leafClause)
        return self


class Bool(ESCompoundClause):

    def __init__(self, ext=dict()):
        super(Bool, self).__init__()
        self['bool'] = dict(**ext)

    def _append(self, key, leafClause):
        if not hasattr(self['bool'], key):
            self['bool'][key] = []

        if isinstance(leafClause, list):
            self['bool'][key] = self['bool'][key] + leafClause
        else:
            self['bool'][key].append(leafClause)

    def must(self, leafClause):
        self._append('must', leafClause)
        return self

    def must_not(self, leafClause):
        self._append('must_not', leafClause)
        return self

    def filter(self, leafClause):
        self._append('filter', leafClause)
        return self 

    def should(self, leafClause, minimum_match = 1):
        self._append('should', leafClause)
        self['bool']['minimum_should_match'] = minimum_match
        return self


class FunctionScore(ESCompoundClause):

    def __init__(self, score_mode='multiply', boost_mode='multiply', ext=dict()):
        super(FunctionScore, self).__init__()
        self['function_score'] = dict(functions=[], boost_mode=boost_mode, score_mode=score_mode, **ext)
    
    def query(self, clause):
        self['function_score']['query'] = clause
        return self

    def decay(self, name, field, origin, scale, offset=0.0, decay=0.5):
        assert(name == 'linear' or name == 'exp' or name =='gauss')        
        func = dict()
        func[name] = dict()
        func[name][field] = dict(
            origin = origin,
            scale = scale,
            offset = offset,
            decay = decay
        )
        self._add_function(func)
        return self

    def weight(self, filter=None, weight=1.0):
        assert(isinstance(filter, ESLeafClause))
        func = dict()
        func['filter'] = filter
        func['weight'] = weight
        self._add_function(func)
        return self
    
    def script(self, script_clause):
        self._add_function(script_clause)
        return self

    def _add_function(self, func):
        self['function_score']['functions'].append(func)


# s = Bool().must([
#     Term('title', 'asd'), 
#     Terms('name', ['x', 'y', 'z']),
#     Range('age', dict(gte=10, lt=20), boost=2.0)])
# print(s)

# s = FunctionScore().query(Term('title', 'ass')).weight(filter=Term('asd','asd'), weight=2.0).script(Script(script='sadas'))
# print(s)