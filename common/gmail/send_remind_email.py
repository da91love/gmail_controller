from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from operator import itemgetter
from datetime import datetime
import pydash as _
import logging

from common.lib.ma.data_access.system.AccessService import AccessService
from api_gmail_remind_sender.const.mail_info import mail_info
from common.const.EMAIL import *

# call instancese
logger = logging.getLogger()

def send_remind_email(sender_email, receiver_email, mail_subject, mail_body, gmail_thread_id):
    """

    :param sender_email:
    :param receiver_email:
    :param mail_subject:
    :param mail_body:
    :param author_unique_id:
    :return:
    """
    try:
        authenticate = Authenticate()
        creds = authenticate.get_authenticate()
        service = build('gmail', 'v1', credentials=creds)

        # Create the Gmail API message with the existing threadId
        raw_message = _create_message(sender_email, receiver_email, mail_subject, mail_body, gmail_thread_id)

        # Send the message
        sent_message = service.users().messages().send(userId='me', body=raw_message).execute()

        return {
            'gmail_thread_id': gmail_thread_id,
            'gmail_msg_id': sent_message.get('id')
        }

    except Exception as e:
        raise e

def _create_message(receiver_email, mail_subject, mail_body, thread_id):
    message = MIMEMultipart()
    message['to'] = receiver_email
    message['mail_subject'] = mail_subject
    # message['threadId'] = thread_id

    # Attach the HTML body
    body_html = MIMEText(mail_body, 'html')
    message.attach(body_html)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message, 'threadId': thread_id}
