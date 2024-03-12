from bs4 import BeautifulSoup

from common.util.EncodingUtil import EncodingUtil
from common.util.StrUtil import StrUtil

def get_gmail_contents(mail_thread_obj):
    try:
        encode_data_of_mail_body = mail_thread_obj.get('payload').get('parts')[0].get('body').get('data')

        if encode_data_of_mail_body:
            decoded = EncodingUtil.encode_byte_to_str(encode_data_of_mail_body)

            if StrUtil.is_html(decoded):
                soup = BeautifulSoup(decoded, "html.parser")

                # Extract text from the parsed HTML
                text = soup.get_text()

                return text
            else:
                return decoded
        else:
            return mail_thread_obj.get('snippet')

    except TypeError:
        return mail_thread_obj.get('snippet')

    except Exception as e:
        raise e



