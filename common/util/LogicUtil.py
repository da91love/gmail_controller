import re

class LogicUtil:
    def count_character(text):
        if text == None:
            return 0
        else:
            count = 0

            for i in text:
                count += len(i)

            return count

    @staticmethod
    def extract_email(text):
        # Define a regular expression pattern for matching email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # Find all matches in the text
        matches = re.findall(email_pattern, text)
        email = matches[0] if matches else None

        # Print the extracted email addresses
        return email