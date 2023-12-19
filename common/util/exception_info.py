import sys
from requests.exceptions import RequestException
from common.type.Errors import IrrelevantParamException
from common.type.Errors import DataLockException
from common.type.Errors import AuthenticationException

def exception_info(exception):

    type, message, trackback = sys.exc_info()

    if isinstance(exception, IrrelevantParamException):
        errorCode = 420
        category = "Input Parameter Error"

    # 参照しようとしたデータがロックされている時のエラー
    if isinstance(exception, DataLockException):
        errorCode = 421
        category = "Data Lock Error"

    # 認証エラー
    if isinstance(exception, AuthenticationException):
        errorCode = 401
        category = "Authentication is overdue or does not exist"

    # # psycopg2モジュールに関する、DB関連のエラー
    # elif isinstance(exception, Psycopg2Exception):
    #     errorCode = 461
    #     category = "psycopg2 Error"

    # requestsモジュールに関する、API通信のエラー
    elif isinstance(exception, RequestException):
        errorCode = 462
        category = "requests Error"

    # その他のPythonのエラー
    elif isinstance(exception, Exception):
        errorCode = 500
        category = "Internal Server Error"

    else:
        errorCode = 470
        category = "Exception"

    except_info = {
        "errorCode": errorCode,
        "type": type,
        "message": message,
        "category": category
    }

    return except_info
