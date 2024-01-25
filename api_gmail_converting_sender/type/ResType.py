from common.type.BaseResType import BaseResType

class ResType(BaseResType):
    def __init__(self, data):
        super().__init__()

        self.set_payload({
            'data': data
        })
