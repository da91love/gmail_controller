import redis
import logging
from common.util.config_get import get_config

# Set config
config = get_config()

# call instancese
logger = logging.getLogger()


class Redis:

    connInstance = None

    @classmethod
    def getConnInstance(cls):
        try:
            if cls.connInstance is None:
                cls.__setConnInstance()

            return cls.connInstance

        except Exception as e:
            raise e

    @classmethod
    def __setConnInstance(cls):
        try:
            logger.info('connRedis starts')

            # Get configuration of DB
            redis_conf = config['REDIS']

            redis_host = redis_conf.get('redis_host')
            redis_port = redis_conf.get('redis_port')
            redis_token = redis_conf.get('redis_token', None)
            redis_ssl = redis_conf.get('redis_ssl', False)

            conn = redis.Redis(
                host=redis_host,
                port=redis_port,
                charset="utf-8",
                decode_responses=True,
                ssl=redis_ssl,
                password=redis_token,
            )

            logger.info('connRedis ends')
            cls.connInstance = conn

        except Exception as e:
            raise e
