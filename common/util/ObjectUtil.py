import pydash as _
import math
class ObjectUtil():
    @staticmethod
    def is_obj(obj, key):
        return obj.get(key)