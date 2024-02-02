import re


class StrUtil:
    @staticmethod
    def clean_mail_body(text):
        # Use regular expression to remove lines starting with ">"
        remove_quote = re.sub(r'^>.*$', '', text, flags=re.MULTILINE)
        remove = remove_quote.replace('\r', '').replace('\n', '')
        escaped_value = remove.replace("'", "''")
        return escaped_value