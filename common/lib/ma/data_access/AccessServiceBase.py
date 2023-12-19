from common.lib.db.mysql.Mysql import Mysql
import logging

# call instancese
logger = logging.getLogger()

class AccessServiceBase:

    @classmethod
    def execute_sql(cls, sql, bindings=None):
        """
        :param sql:
        :param bindings:
        :return:
        """
        try:
            logger.info('executeSql starts')

            # Create connection instance
            connection_pool = Mysql.getConnectionPool()
            conn = connection_pool.get_connection()

            # Create a cursor instance
            cursor = conn.cursor(dictionary=True, buffered=True)

            if bindings:
                sql = sql.format(**bindings)

            logger.info(sql)
            cursor.execute(sql)

            try:
                sql_result = cursor.fetchall()

                # Commit
                conn.commit()

                # Close cursor, connection close
                cls.__close(conn, cursor)

                logger.info('executeSql ends')

                return sql_result

            # Exception occurs when fetchall insert result
            except BaseException:
                # Commit
                conn.commit()

                # Close cursor, connection close
                cls.__close(conn, cursor)

                logger.info('executeSql ends')
                pass

        except Exception as e:
            conn.rollback()

            # Close cursor, connection close
            cls.__close(conn, cursor)

            raise e

    @classmethod
    def __close(cls, conn, cursor):
        try:
            # Close cursor, connection close
            cursor.close()
            logger.info('cursor closed')

            conn.close()
            logger.info('connection closed')

        except Exception as e:
            raise e
