import logging
from common.util.config_get import get_config
import psycopg2

# Set config
config = get_config()

# call instancese
logger = logging.getLogger()


class Postgre:

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
            logger.info('connPostgre starts')

            # Get configuration of DB
            pgConf = config['DB']['postgre']

            rds_host = pgConf['db_host']
            rds_database = pgConf['db_database']
            rds_port = pgConf['db_port']
            rds_password = pgConf['db_password']
            rds_user = pgConf['db_user']
            rds_sslmode = pgConf.get('db_sslmode', None)
            rds_sslrootcert = pgConf.get('db_sslrootcert', None)

            conn = psycopg2.connect(
                host=rds_host,
                database=rds_database,
                port=rds_port,
                user=rds_user,
                password=rds_password,
                sslmode=rds_sslmode,
                sslrootcert=rds_sslrootcert,
            )

            logger.info('connPostgre ends')
            cls.connInstance = conn

        except Exception as e:
            raise e
