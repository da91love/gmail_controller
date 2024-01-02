from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import pydash as _

from common.type.Errors import PicNotAssignedException

def modify_label(gmail_msg_id, add_label_names, remove_label_names):
    try:
        authenticate = Authenticate()
        creds = authenticate.get_authenticate()
        service = build('gmail', 'v1', credentials=creds)

        labels = service.users().labels().list(userId='me').execute()

        add_label_ids = [(_.filter_(labels['labels'], {'name': label_name})) [0]['id']for label_name in add_label_names]
        remove_label_ids = [(_.filter_(labels['labels'], {'name': label_name}))[0]['id'] for label_name in remove_label_names]

        modified_label_ids = {
            'removeLabelIds': [remove_label_ids],
            'addLabelIds': [add_label_ids],
        }

        service.users().messages().modify(userId='me', id=gmail_msg_id, body=modified_label_ids).execute()

    except IndexError as e:
        raise PicNotAssignedException

    except Exception as e:
        raise e
