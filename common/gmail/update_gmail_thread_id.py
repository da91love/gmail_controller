from operator import itemgetter

from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *
from common.const.STATUS import *

def update_gmail_thread_id(old_gmail_thread_id, new_gmail_thread_id):
    try:
        print('new_gmail_thread_id: ' + new_gmail_thread_id)
        print('old_gmail_thread_id: ' + old_gmail_thread_id)

        # mail contents
        AccessService(GLOBAL).update_gmail_mail_contents_thread_id(
            new_gmail_thread_id=new_gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

        # mail contact
        AccessService(GLOBAL).update_gmail_mail_contact_thread_id(
            new_gmail_thread_id=new_gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

    except Exception as e:
        raise e