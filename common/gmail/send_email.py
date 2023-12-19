from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from datetime import datetime

from common.lib.ma.data_access.system.AccessService import AccessService

def send_email(sender_email, receiver_email, mail_subject, mail_body, author_unique_id, tiktok_url):
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

        # Create the Gmail API message
        raw_message = _create_message(sender_email, receiver_email, mail_subject, mail_body)

        # Send the message
        sent_message = service.users().messages().send(userId='me', body=raw_message).execute()

        # Get the current date and time
        gmail_thread_id = sent_message.get("threadId")
        gmail_msg_id = sent_message.get("id")
        gmail_label_id = sent_message.get("labelId")
        formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # insert to contact db
        AccessService.insert_contact_history(
            gmail_thread_id=gmail_thread_id,
            gmail_msg_id=gmail_msg_id,
            gmail_label_id='SENT',
            sender_email= sender_email,
            receiver_email= receiver_email,
            contents='',
            create_at=formatted_datetime
        )

        # insert to infl info db
        AccessService.insert_infl_info(
            gmail_thread_id=gmail_thread_id,
            author_unique_id=author_unique_id,
            receiver_email=receiver_email,
            tiktok_url=tiktok_url
        )

        return {
            'gmail_thread_id': gmail_thread_id,
            'gmail_msg_id': gmail_msg_id,
        }

    except Exception as e:
        raise e

def _create_message(sender, to, subject, body):
    try:
        """Create a MIMEText message for an email."""
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(body, 'html')
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        return {'raw': raw_message}
    except Exception as e:
        raise e
