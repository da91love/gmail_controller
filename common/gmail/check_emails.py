from googleapiclient.discovery import build
from datetime import datetime
from operator import itemgetter
import pydash as _

from common.util.logger_get import get_logger

from common.lib.ma.data_access.system.AccessService import AccessService
from common.gmail.Authenticate import Authenticate
from common.util.DateUtil import DateUtil
from common.const.EMAIL import *
from common.util.LogicUtil import LogicUtil
from common.gmail.LabelControl import LabelControl

# Create instances
logger = get_logger()

def check_emails(label_id):
    try:
        authenticate = Authenticate()
        creds = authenticate.get_authenticate()

        # 최근 15개까지 받은 메일 쓰레드 id 표시
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=[label_id], maxResults=10).execute()
        msg_metas = results.get('messages', [])
        gmail_thread_ids = _.uniq([msg['threadId'] for msg in msg_metas])

        new_arrival_mails = []
        if not msg_metas:
            print('No messages found.')
        else:
            # 획득한 쓰레드 ID Loop
            for gmail_thread_id in gmail_thread_ids:
                try:
                    # db에서 thread_id로 contact 횟수 검색
                    contact_history = AccessService.select_contacts(gmail_thread_id=gmail_thread_id)

                    # db에 등록된 메일 처리
                    # db에 등록되지 않을 mail이 검색됐을 때 무시하기위해 len(contact_history) > 0 조건 추가
                    if len(contact_history) > 0:
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
                                        t_key = (contact_history[0]).get('t_key')

                                        result = {
                                            'gmail_thread_id': gmail_thread_id,
                                            'gmail_msg_id': new_gmail_msg_id,
                                            'gmail_label_id': label_id,
                                            't_key': t_key,
                                            'contents': contents,
                                            'created_at': created_at
                                        }

                                        # put in into result
                                        new_arrival_mails.append(result)

                    # SENT 일 시 이미 쓰레드를 타고 있기 때문에 abnormal thread handling 필요없음
                    elif len(contact_history) > 0 and label_id == 'INBOX':
                        mails_in_thread = service.users().threads().get(userId='me', id=gmail_thread_id).execute()
                        msgs_in_thread = mails_in_thread.get('messages')

                        # 메일 스레드의 처음 시작이 eqqualberry.comm 이 맞는지 확인
                        sender_list = _.filter_(msgs_in_thread[0]['payload']['headers'], lambda x: x['name'] in ['from', 'From'])
                        receiver_list = _.filter_(msgs_in_thread[0]['payload']['headers'], lambda x: x['name'] in ['to', 'To'])

                        sender_in_mail_value_thread = sender_list[0].get('value') if len(sender_list) > 0 else None
                        receiver_in_mail_value_thread = receiver_list[0].get('value') if len(receiver_list) > 0 else None

                        sender_in_mail_thread = LogicUtil.extract_email(sender_in_mail_value_thread)
                        receiver_in_mail_thread = LogicUtil.extract_email(receiver_in_mail_value_thread)

                        if sender_in_mail_thread == SENDER_EMAIL:
                            # 기존 thread id 검색
                            old_gmail_thread_info = AccessService.select_thread_id_by_email(receiver_email=receiver_in_mail_thread)

                            # old_gmail_thread_info 0일 경우: db에서 이메일 검색이 안될 시 우리가 컨택한적 없는 외부 컨택이므로 무시 혹은 시스템 구축 전 수동으로 보낸 메일이므로 무시
                            # old_gmail_thread_info 1보다 클 경우: 정상적인 플로우라면 old_gmail_thread_info 한 건만 검색되어야 하는데 복수건 검색될 경우 update시 primary에러 발생하므로 무시
                            if len(old_gmail_thread_info) == 1:
                                old_gmail_thread_id, t_key = itemgetter('gmail_thread_id', 't_key')(old_gmail_thread_info[0])

                                # 기존 thread id update
                                AccessService.update_gmail_mail_contact_thread_id(new_gmail_thread_id=gmail_thread_id, old_gmail_thread_id=old_gmail_thread_id)
                                AccessService.update_gmail_contact_status_thread_id(new_gmail_thread_id=gmail_thread_id, old_gmail_thread_id=old_gmail_thread_id)

                                # gmail label update
                                # modify label
                                new_gmail_msg_id = _.last(msgs_in_thread).get('id')

                                status_data = AccessService.select_contacts_status(gmail_thread_id=gmail_thread_id)
                                status, progress = itemgetter('status', 'progress')(status_data[0])

                                pic = (AccessService.select_pic(t_key=t_key)[0])['pic']

                                LabelControl().add_label(gmail_msg_id=new_gmail_msg_id, add_label_names=[status, progress, pic])

                                for msg_in_thread in msgs_in_thread:
                                    # 파라미터로 전해진 labelId로 필터링
                                    if label_id in msg_in_thread['labelIds']:
                                        gmail_msg_id = msg_in_thread.get('id')
                                        created_at = DateUtil.format_milliseconds(msg_in_thread.get('internalDate'),
                                                                                  '%Y-%m-%d %H:%M:%S')
                                        contents = msg_in_thread.get('snippet')

                                        result = {
                                            'gmail_thread_id': gmail_thread_id,
                                            'gmail_msg_id': gmail_msg_id,
                                            'gmail_label_id': label_id,
                                            't_key': t_key,
                                            'contents': contents,
                                            'created_at': created_at
                                        }

                                        # put in into result
                                        new_arrival_mails.append(result)

                except IndexError:
                    logger.error('error in gmail thread check')
                    continue

        return new_arrival_mails
    except Exception as e:
        raise e

