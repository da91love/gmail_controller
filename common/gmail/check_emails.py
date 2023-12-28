from googleapiclient.discovery import build
from datetime import datetime

from common.lib.ma.data_access.system.AccessService import AccessService
from common.gmail.Authenticate import Authenticate
from common.util.DateUtil import DateUtil

def check_emails(label_id):
    try:
        authenticate = Authenticate()
        creds = authenticate.get_authenticate()

        # 최근 5개까지 받은 메일 쓰레드 id 표시
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=15).execute()
        msg_metas = results.get('messages', [])

        new_arrival_mails = []
        if not msg_metas:
            print('No messages found.')
        else:
            # 획득한 15개 쓰레드 ID Loop
            for msg_meta in msg_metas:
                gmail_thread_id = msg_meta.get('threadId')

                # db에서 thread_id로 contact 횟수 검색
                contact_history = AccessService.select_contact_num(gmail_thread_id=gmail_thread_id)

                # db에 등록되지 않을 mail이 검색됐을 때 무시하기위해 len(contact_history) > 0 조건 추가
                if len(contact_history) > 0:

                    # get emails by threadId
                    mails_in_thread = service.users().threads().get(userId='me', id=gmail_thread_id).execute()
                    msgs_in_thread = mails_in_thread.get('messages')

                    # mail thread 개수가 db 內 컨택 개수보다 많을 시 새로운 메일이 도착했다는 의미의 조건식
                    if len(msgs_in_thread) > len(contact_history):
                        msg_ids_fr_db = [ i['gmail_msg_id'] for i in contact_history]

                        for msg_in_thread in msgs_in_thread:
                            # db에는 등록되지 않은 신규 msg id 필터링
                            if msg_in_thread['id'] not in msg_ids_fr_db:
                                # 파라미터로 전해진 labelId로 필터링
                                if label_id in msg_in_thread['labelIds']:

                                    new_gmail_msg_id = msg_in_thread.get('id')
                                    created_at = DateUtil.format_milliseconds(msg_in_thread.get('internalDate'), '%Y-%m-%d %H:%M:%S')
                                    contents = msg_in_thread.get('snippet')
                                    receiver_email = (contact_history[0]).get('receiver_email')
                                    author_unique_id = (contact_history[0]).get('author_unique_id')
                                    seeding_num = (contact_history[0]).get('seeding_num')

                                    result = {
                                        'gmail_thread_id': gmail_thread_id,
                                        'gmail_msg_id': new_gmail_msg_id,
                                        'gmail_label_id': label_id,
                                        'author_unique_id': author_unique_id,
                                        'seeding_num': seeding_num,
                                        'contents': contents,
                                        'created_at': created_at
                                    }

                                    # put in into result
                                    new_arrival_mails.append(result)

        return new_arrival_mails
    except Exception as e:
        raise e

