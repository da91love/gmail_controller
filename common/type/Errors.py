class PicNotAssignedException(Exception):
    # 例外情報をもらってメッセージを出せるか
    def __init__(
            self,
            msg="Pic is not assigned"):
        Exception.__init__(self, msg)

class IrrelevantParamException(Exception):
    # 例外情報をもらってメッセージを出せるか
    def __init__(
            self,
            msg="Requested parameter is not enough"):
        Exception.__init__(self, msg)

class DataLockException(Exception):
    def __init__(
            self,
            msg="The request could not be completed due to a conflict with the current state of the resource."):
        Exception.__init__(self, msg)


class AuthenticationException(Exception):
    def __init__(self, msg="Token is not valid."):
        Exception.__init__(self, msg)


class WrongSessionException(Exception):
    def __init__(
            self,
            msg="Session Ends or Wrong session. lock_id is not relevant."):
        Exception.__init__(self, msg)


class WrongParameterException(Exception):
    def __init__(self, msg="Parameter is wrong"):
        Exception.__init__(self, msg)


class RollbackTrnException(Exception):
    def __init__(
            self,
            msg="The request could not be completed because one or more transaction failed."):
        Exception.__init__(self, msg)


class WrongSessionException(Exception):
    def __init__(
            self,
            msg="Session Ends or Wrong session. lock_id is not relevant."):
        Exception.__init__(self, msg)


class WrongResponseException(Exception):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)


class WrongConfigEnvironmentException(Exception):
    def __init__(
            self,
            msg="Environment variable for config setup is not relevant."):
        Exception.__init__(self, msg)


class QueryParamInsufficientException(Exception):
    def __init__(self, msg="Query parameter is insufficient."):
        Exception.__init__(self, msg)


class AuthenticationException(Exception):
    def __init__(self, msg="Insufficient authentication."):
        Exception.__init__(self, msg)


class WrongApiResponseException(Exception):
    def __init__(self, msg="Wrong api response"):
        Exception.__init__(self, msg)


class NoValueFilteredByQueryStringException(Exception):
    def __init__(self, msg="No value was found with querystring"):
        Exception.__init__(self, msg)
