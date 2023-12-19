class BaseRes:
    """
    __init__ function : initiate function
    """

    def __init__(self):
        self.base_res = {
            "status": 'success',
            "payload": None,
            "api-version": 'v1.01.1'
        }

    def get_res(self):
        return self.base_res
