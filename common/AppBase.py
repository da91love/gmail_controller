import traceback

from common.util.get_config import get_config
from common.util.exception_info import exception_info
from common.type.ErrorRes import ErrorRes
from common.util.logger_get import get_logger
# from common.lib.db.redis.Redis import Redis
from common.type.Errors import AuthenticationException

# Create instances
config = get_config()
logger = get_logger()
# redis = Redis.getConnInstance()
logger.info(config['name'])

class AppBase:
    def __init__(self, func):
        """
        function
        :param func: decorator target
        """
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        function
        :param args:
        :param kwargs:
        :return:
        """
        try:
            # Get data from API Gateway
            # if redis.hget('token', args['params']['header']['tokenId']):
            if True:
                logger.info(f'{self.func.__name__} starts')
                r = self.func(*args, **kwargs)
                logger.info(f'{self.func.__name__} ends')

                return r

            else:
                raise AuthenticationException

        except Exception as e:
            logger.error(traceback.format_exc())
            except_info = exception_info(e)
            error_res = ErrorRes(
                errorCode=except_info['errorCode'],
                type=str(except_info['type']),
                message=str(except_info['message']),
                category=str(except_info['category'])
            ).get_res()
            logger.error(error_res)
            return error_res
