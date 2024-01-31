from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.EncodingUtil import EncodingUtil
from common.util.logger_get import get_logger

config = get_config()
logger = get_logger()


api_key = config['TIKAPI']['api_key']
account_key = config['TIKAPI']['account_key']
api = TikAPI(api_key)
User = api.user(accountKey=account_key)


encode_data_of_mail_body = 'CjxkaXY-SGVsbG8sIG1hbWFtb2NoaTEyLDwvZGl2Pgo8YnIvPgo8ZGl2PkkgYW0gSmVubmlmZXIhIEhvdyB3YXMgeW91IHdlZWtlbmQ_IPCfjIg8L2Rpdj4KPGJyLz4KPGRpdj5JZiB5b3UgaGF2ZSBhbnkgdXBkYXRlLCBwbGVhc2UgZm9sbG93IHVwIHRoaXMgZW1haWwhPC9kaXY-CjxkaXY-VGhhbmsgeW91IGZvciB5b3VyIGhlbHDwn5iJPC9kaXY-Cjxici8-CjxkaXY-V2FybWVzdCByZWdhcmRzLCDwn4y3SmVubmlmZXI8L2Rpdj4KCjxzcGFuPiZuYnNwOzwvc3Bhbj4KPGRpdj5UaWt0b2s6IEBlcXF1YWxiZXJyeV91czwvZGl2Pgo8ZGl2Pkluc3RhZ3JhbTogZXFxdWFsYmVycnlfdXM8L2Rpdj4K'
ll = EncodingUtil.encode_byte_to_str(encode_data_of_mail_body)
print(ll)

#     response = api.public.search(
#         category="general",
#         query="cosrx",
#         country='us'
#     )
#
#     while(response):
#         res = response.json()
#         nextCursor = response.json().get('nextCursor')
#         print("Getting next items ", nextCursor)
#         response = response.next_items()
#
# except ValidationException as e:
#     print(e, e.field)
#
# except ResponseException as e:
#     print(e, e.response.status_code)


