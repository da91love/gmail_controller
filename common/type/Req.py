class Req_frmt:

    __payload = {
        "domain": None,
        "snapshot": None,
        "lock": None,
        "table_select": None,
        "session": {
            "lock": None,
            "trx": None
        },
        "busiDate": None,
        "data": None
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
            domain=None,
            lock=None,
            snapshot=None,
            lockId=None,
            trxId=None,
            busiDate=None,
            table_select=None,
            data=None):
        self.__payload['domain'] = domain or None
        self.__payload['lock'] = lock or None
        self.__payload['table_select'] = table_select or None
        self.__payload['snapshot'] = snapshot or None
        self.__payload['session']['lock'] = lockId or None
        self.__payload['session']['trx'] = trxId or None
        self.__payload['busiDate'] = busiDate or None
        self.__payload['data'] = data or None

    def getReq(self):
        return self.__payload
