class BaseResType:
    """
    __init__ function : initiate function
    """

    def __init__(self):
        self.status: str = 'success'
        self.payload: any = None
        self.api_version: str = 'v1.01.1'

    def set_payload(self, payload):
        self.payload = payload

    def get_response(self):
        return {
            'status': self.status,
            'payload': self.payload,
            'apiVersion': self.api_version
        }

    # def set_status(self, status):
    #     self.status = status
    #
    # def set_payload(self, payload):
    #     self.payload = payload
    #
    # def set_api_version(self, api_version):
    #     self.api_version = api_version
    #
    # def get_all_as_dict(self):
    #     return {
    #         'status': self.status,
    #         'payload': self.payload,
    #         'api_version': self.api_version,
    #     }
