class ApiHandler:
    filters = []

    def __init__(self, filters = None):
        if filters is not None:
            self.filters = filters
    
    # return byte, error_code
    def process(self, args, context=None):
        return None, 'Empty_Api'

