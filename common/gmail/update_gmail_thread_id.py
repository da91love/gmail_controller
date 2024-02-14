from operator import itemgetter

from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.STATUS import *

def update_gmail_thread_id(old_gmail_thread_id, new_gmail_thread_id):
    try:
        print('new_gmail_thread_id: ' + new_gmail_thread_id)
        print('old_gmail_thread_id: ' + old_gmail_thread_id)

        # status
        ## 기존 status 데이터 취득
        old_status_info = AccessService.select_contacts_status(gmail_thread_id=old_gmail_thread_id)
        status, progress = STATUS['OPEN'], PROGRESS['NEGOTIATING']
        if len(old_status_info) > 0:
            status, progress = itemgetter('status', 'progress')(old_status_info[0])

        ## 기존꺼 삭제
        AccessService.delete_temp_status(old_gmail_thread_id=old_gmail_thread_id)
        ## 새로운거 없으면 추가
        contact_status = AccessService.select_contacts_status(gmail_thread_id=new_gmail_thread_id)
        if len(contact_status) < 1:
            AccessService.insert_contact_status(
                gmail_thread_id=new_gmail_thread_id,
                status=status,
                progress=progress
            )

        # slack
        AccessService.update_slack_thread_id(
            new_gmail_thread_id=new_gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

        # mail contents
        AccessService.update_gmail_mail_contents_thread_id(
            new_gmail_thread_id=new_gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

        # mail contact
        AccessService.update_gmail_mail_contact_thread_id(
            new_gmail_thread_id=new_gmail_thread_id,
            old_gmail_thread_id=old_gmail_thread_id
        )

    except Exception as e:
        raise e