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

# call instancese
logger = logging.getLogger()

def send_remind_email():
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

        # get thread_id
        tg_contacts = AccessService.select_sent_thread_id()

        # Group data by threadId
        grouped_data = _.group_by(tg_contacts, "gmail_thread_id")

        # Extract the latest entry for each threadId
        latest_sent_contacts = [_.max_by(group, lambda x: x["created_at"]) for group in grouped_data.values()]

        re_sent_mails = []
        for latest_sent_contact in latest_sent_contacts:
            gmail_thread_id, gmail_msg_id, sender_email, receiver_email, created_at \
                = itemgetter('gmail_thread_id', 'gmail_msg_id', 'sender_email', 'receiver_email', 'created_at')(latest_sent_contact)

            sent_num = len(grouped_data[gmail_thread_id])

            # if sent number is over 3, no remind send
            if sent_num < 3:
                # remind if over 5 days # TODO: change days diff
                if (datetime.now() - created_at).days >= 5:

                    # Extract the information you need, e.g., sender, receiver, subject, etc.
                    sender_email = sender_email
                    receiver_email = receiver_email
                    subject = mail_info[sent_num-1]['mail_subject']
                    body = mail_info[sent_num-1]['mail_body']
                    formatted_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Create the Gmail API message with the existing threadId
                    raw_message = _create_message(sender_email, receiver_email, subject, body, gmail_thread_id)

                    # Send the message
                    sent_message = service.users().messages().send(userId='me', body=raw_message).execute()

                    # insert to contact db
                    AccessService.insert_contact_history(
                        gmail_thread_id=gmail_thread_id,
                        gmail_msg_id=sent_message.get('id'),
                        gmail_label_id='SENT',
                        sender_email=sender_email,
                        receiver_email=receiver_email,
                        contents='',
                        created_at=formatted_datetime
                    )

                    re_sent_mails.append({
                        'gmail_thread_id': gmail_thread_id,
                        'gmail_msg_id': gmail_msg_id,
                    })

        return re_sent_mails

    except Exception as e:
        raise e

def _create_message(sender, to, subject, body, thread_id):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    # message['threadId'] = thread_id

    # Attach the HTML body
    body_html = MIMEText(body, 'html')
    message.attach(body_html)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message, 'threadId': thread_id}
