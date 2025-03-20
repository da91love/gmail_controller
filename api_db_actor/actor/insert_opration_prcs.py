from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *

def insert_opration_prcs(data):
    try:
        AccessService(GLOBAL).truncate_invoice_master()
        AccessService(GLOBAL).insert_invoice_master(data)
    except Exception as e:
        raise e