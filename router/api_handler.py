class ApiHandler:
    _filters = []

    def __init__(self, filters = None):
        if filters is not None:
            self._filters = filters
        

    def filters(self):
        return self._filters
    
    # return byte, error_code
    def process(self, args, context=None):
        return None, 'Empty_Api'

