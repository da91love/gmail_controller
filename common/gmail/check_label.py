from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import pydash as _

from common.type.Errors import PicNotAssignedException

def check_label(gmail_msg_id, sender_email):
    try:
        authenticate = Authenticate(sender_email)
        creds = authenticate.get_authenticate()
        service = build('gmail', 'v1', credentials=creds)

        # ID of the message (email) you want to check labels for
        message_id = gmail_msg_id

        # Get the metadata of the specified message
        message = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
        labels = message['labelIds']

        return labels

    except IndexError as e:
        raise PicNotAssignedException

    except Exception as e:
        raise e
