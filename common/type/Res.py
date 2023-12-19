class Res_frmt:

    __payload = {
        "status": None,
        "payload": {
            "session": {
                "lock": None,
                "trx": None
            },
            "busiDate": None,
            "data": None,
        },
        "api-version": None
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
            status='success',
            lock=None,
            trx=None,
            busiDate=None,
            data=None,
            api_version='v1.01.1'):
        self.__payload['status'] = status
        self.__payload['payload']['session']['lock'] = lock
        self.__payload['payload']['session']['trx'] = trx
        self.__payload['payload']['busiDate'] = busiDate
        self.__payload['payload']['data'] = data
        self.__payload['api-version'] = api_version

    def get_res(self):
        return self.__payload
