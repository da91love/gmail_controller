from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *

def insert_invoice_master(data):
    try:
       AccessService(GLOBAL).insert_invoice_master(data)
    except Exception as e:
        raise e