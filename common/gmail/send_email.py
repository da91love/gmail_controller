from googleapiclient.discovery import build
from common.gmail.Authenticate import Authenticate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_email(sender_email, receiver_email, mail_subject, mail_body):
    """

    :param sender_email:
    :param receiver_email:
    :param mail_subject:
    :param mail_body:
    :param author_unique_id:
    :return:
    """
    try:
        authenticate = Authenticate(sender_email)
        creds = authenticate.get_authenticate()
        service = build('gmail', 'v1', credentials=creds)

        # Create the Gmail API message
        raw_message = _create_message(sender_email, receiver_email, mail_subject, mail_body)

        # Send the message
        sent_message = service.users().messages().send(userId='me', body=raw_message).execute()

        return sent_message

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
