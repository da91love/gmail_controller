class CallbackReq:

    __payload = {
        "busiDate": None,
        "data": None,
        "tId": None,
        "cbStatus": None,
        "progress": None,
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
            busiDate=None,
            data=None,
            cbStatus=None,
            tId=None,
            progress=None):
        self.__payload['busiDate'] = busiDate
        self.__payload['data'] = data
        self.__payload['cbStatus'] = cbStatus
        self.__payload['tId'] = tId
        self.__payload['progress'] = progress

    def get_req(self):
        return self.__payload
