class ErrorRes:

    __payload = {
        "status": None,
        "errorCode": None,
        "type": None,
        "message": None,
        "category": None
    }

    """
    __init__ function : initiate function
        :param domain: string
        :param snapshot: string
        :param session: dict
        :param data: dict
    """

    def __init__(
            self,
            status="fail",
            errorCode=None,
            type=None,
            message=None,
            category=None):
        self.__payload['status'] = status
        self.__payload['errorCode'] = errorCode or None
        self.__payload['type'] = type or None
        self.__payload['message'] = message or None
        self.__payload['category'] = category or None

    def get_res(self):
        return self.__payload
