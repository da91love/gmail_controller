import re

class StrUtil:
    @staticmethod
    def clean_mail_body(text):
        # Use regular expression to remove lines starting with ">"
        remove_quote = re.sub(r'^>.*$', '', text, flags=re.MULTILINE)
        remove = remove_quote.replace('\r', '').replace('\n', '')
        # escaped_value = remove.replace("'", "''")
        return remove

    @staticmethod
    def is_html(content):
        return any(tag in content for tag in ("<html>", "<body>", "<div>", "<p>", "<a>"))
