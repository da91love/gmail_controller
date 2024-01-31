from common.util.EncodingUtil import EncodingUtil

def get_gmail_contents(mail_thread_obj):
    try:
        encode_data_of_mail_body = mail_thread_obj.get('payload').get('body').get('data')

        if encode_data_of_mail_body:
            return EncodingUtil.encode_byte_to_str(encode_data_of_mail_body)
        else:
            return mail_thread_obj.get('snippet')
    except Exception as e:
        raise e



