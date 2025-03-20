from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *

def insert_opration_prcs(data):
    try:
        for dt in data:
            doc_type = data[dt].get('docType')
            export_id = data[dt].get('exportNo')
            requester = data[dt].get('requester')

            AccessService(GLOBAL).insert_op_process(
                export_id=export_id,
                doc_type=doc_type,
                requester=requester
            )
    except Exception as e:
        raise e