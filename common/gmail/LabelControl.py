from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import pydash as _

from common.type.Errors import PicNotAssignedException
from common.const.DEFAULT_LABEL import DEFAULT_LABEL

class LabelControl:
    def __init__(self, sender_email):
        authenticate = Authenticate(sender_email)
        creds = authenticate.get_authenticate()
        self.service = build('gmail', 'v1', credentials=creds)

    def check_label(self, gmail_msg_id):
        try:

            # ID of the message (email) you want to check labels for
            message_id = gmail_msg_id

            # Get the metadata of the specified message
            message = self.service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
            labels = message['labelIds']

            return labels

        except IndexError as e:
            raise PicNotAssignedException

        except Exception as e:
            raise e

    def add_label(self, gmail_msg_id, add_label_names = None, add_label_ids = None):
        try:
            labels = self.service.users().labels().list(userId='me').execute()

            add_labels_as_id = add_label_ids or [(_.filter_(labels['labels'], {'name': label_name}))[0]['id'] for label_name in add_label_names]

            modified_label_ids = {
                'addLabelIds': add_labels_as_id,
            }

            self.service.users().messages().modify(userId='me', id=gmail_msg_id, body=modified_label_ids).execute()

        except IndexError as e:
            raise PicNotAssignedException

        except Exception as e:
            raise e
    def remove_label(self, gmail_msg_id, remove_label_names = None, remove_label_ids = None):
        try:
            labels = self.service.users().labels().list(userId='me').execute()

            remove_labels_as_id = remove_label_ids or [(_.filter_(labels['labels'], {'name': label_name}))[0]['id'] for label_name in remove_label_names]

            # 시스템 라벨은 제거하지 못하도록 필터링
            modify_remove_labels_ad_id = []
            for remove_label in remove_labels_as_id:
                if not _.filter_(DEFAULT_LABEL, {'id':remove_label}):
                    modify_remove_labels_ad_id.append(remove_label)

            modified_label_ids = {
                'removeLabelIds': modify_remove_labels_ad_id,
            }

            # modify_remove_labels_ad_id 비어 있으면 gmail api 에러발생
            if modify_remove_labels_ad_id:
                self.service.users().messages().modify(userId='me', id=gmail_msg_id, body=modified_label_ids).execute()

        except IndexError as e:
            raise PicNotAssignedException

        except Exception as e:
            raise e
