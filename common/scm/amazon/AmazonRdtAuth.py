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

class AmazonRdtAuth:
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
                r = self.func(*args, **kwargs)

                return r

            else:
                raise AuthenticationException

        except Exception as e:
            pass

