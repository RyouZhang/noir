# -*- coding: utf-8 -*-

__author__ = 'lvyi'

ERR_CODE_SERVER_INTERNAL_ERROR = 1999
COMMON_ERROR_MSG = 'Snap! Something\'s gone wrong. Please try again soon.'

ERR_MSG = {
    ERR_CODE_SERVER_INTERNAL_ERROR: COMMON_ERROR_MSG,
}


class FivemilesApiError(Exception):
    def __init__(self, err_code=None, err_msg=None, ext_data=None):
        if not err_code:
            err_code = ERR_CODE_SERVER_INTERNAL_ERROR
        self.err_code = err_code
        self.err_msg = err_msg if err_msg else ERR_MSG.get(self.err_code, COMMON_ERROR_MSG)
        self.ext_data = ext_data

    def __str__(self):
        return u'code: {0}, msg: {1}, {2}'.format(self.err_code, self.err_msg, self.ext_data)


class FuncConfNofoundError(FivemilesApiError):
    def __init__(self, err_msg=None):
        FivemilesApiError.__init__(self, ERR_CODE_SERVER_INTERNAL_ERROR, err_msg)
