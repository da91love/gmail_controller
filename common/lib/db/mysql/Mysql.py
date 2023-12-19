import logging
from common.util.get_config import get_config
import mysql.connector
from mysql.connector import pooling

# Set config
config = get_config()

# call instancese
logger = logging.getLogger()

class Mysql:

    '''
    getConnInstance 은 하나의 db connection만을 생성하기 위해, 싱글톤으로 작성됨.
    하지만 하나의 connection에서 작업을 하다보니, 여러 에러가 수반되게 되어 매 sql마다 새로운 connection을 생성하는 방법으로 변경
    https://stackoverflow.com/questions/65169638/mysqlconnector-python-new-db-connection-for-each-query-vs-one-single-connect
    '''
    connectionPoolInstance = None

    @classmethod
    def getConnectionPool(cls):
        try:
            if cls.connectionPoolInstance is None:
                cls.__setConnectionPool()

            return cls.connectionPoolInstance

        except Exception as e:
            raise e

    @classmethod
    def __setConnectionPool(cls):
        try:
            logger.info('mysql connection pool starts')

            # Get configuration of DB
            pgConf = config['DB']['mysql']

            rds_host = pgConf['db_host']
            rds_database = pgConf['db_database']
            rds_port = pgConf['db_port']
            rds_password = pgConf['db_password']
            rds_user = pgConf['db_user']
            ssl_disabled = pgConf['ssl_disabled']

            connection_pool = pooling.MySQLConnectionPool(pool_name="connection_pool",
                                                          pool_size=3,
                                                          pool_reset_session=True,
                                                          host=rds_host,
                                                          database=rds_database,
                                                          port=rds_port,
                                                          user=rds_user,
                                                          password=rds_password,
                                                          ssl_disabled=ssl_disabled)


            logger.info('mysql connection pool ends')

            cls.connectionPoolInstance = connection_pool

        except Exception as e:
            raise e
