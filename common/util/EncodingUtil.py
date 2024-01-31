import base64

class EncodingUtil:
    @staticmethod
    def encode_byte_to_str(encoded_text):
        encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1']

        decoded_text = None
        for encoding in encodings_to_try:
            try:
                decoded_text = base64.b64decode(encoded_text).decode(encoding)
                break  # Stop if decoding is successful
            except UnicodeDecodeError:
                pass

        return decoded_text
