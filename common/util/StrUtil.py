import re

class StrUtil:
    @staticmethod
    def clean_mail_body(text):
        # Use regular expression to remove lines starting with ">"
        remove_quote = re.sub(r'^>.*$', '', text, flags=re.MULTILINE)
        remove = remove_quote.replace('\r', '').replace('\n', '')
        escaped_value = remove.replace("'", "''")
        return escaped_value

    @staticmethod
    def is_html(content):
        return any(tag in content for tag in ("<html>", "<body>", "<div>", "<p>", "<a>"))

    @staticmethod
    def split_string_into_chunks(text, chunk_size=2500):
        # Initialize an empty list to store the chunks
        chunks = []

        # Calculate the total number of chunks needed
        num_chunks = (len(text) + chunk_size - 1) // chunk_size

        # Split the string into chunks of the specified size
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            chunks.append(text[start_idx:end_idx])

        return chunks