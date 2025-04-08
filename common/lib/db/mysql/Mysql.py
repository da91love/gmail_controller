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
    복수개의 db 접속시에는 dict로 만들어진 connectionPoolInstance에서 db conn 선택
    '''
    connectionPoolInstance: dict = {}

    @classmethod
    def getConnectionPool(cls, db):
        try:
            if (cls.connectionPoolInstance).get(db) is None:
                (cls.connectionPoolInstance)[db] = cls.__setConnectionPool(db)

            return (cls.connectionPoolInstance).get(db)

        except Exception as e:
            raise e

    @classmethod
    def __setConnectionPool(cls, db):
        try:
            logger.info('mysql connection pool starts')

            # Get configuration of DB
            pgConf = config['DB']['mysql'][db]

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

            return connection_pool

        except Exception as e:
            raise e
