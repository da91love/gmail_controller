from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import pydash as _

from common.type.Errors import PicNotAssignedException

def modify_label(gmail_msg_id, label_name):
    try:
        authenticate = Authenticate()
        creds = authenticate.get_authenticate()
        service = build('gmail', 'v1', credentials=creds)

        labels = service.users().labels().list(userId='me').execute()
        on_progress_label_id = (_.filter_(labels['labels'], {'name': 'onProgress'}))[0]['id']

        tg_label_id = (_.filter_(labels['labels'], {'name': label_name}))[0]['id']

        addLabelIds = {'addLabelIds': [on_progress_label_id, tg_label_id]}

        service.users().messages().modify(userId='me', id=gmail_msg_id, body=addLabelIds).execute()

    except IndexError as e:
        raise PicNotAssignedException

    except Exception as e:
        raise e
