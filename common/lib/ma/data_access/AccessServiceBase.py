from common.lib.db.mysql.Mysql import Mysql
import logging

# call instancese
logger = logging.getLogger()

class AccessServiceBase:

    def __init__(self, db):
        self.db = db

    def execute_bulk_sql(self, sql, data):
        """
        :param sql:
        :param bindings:
        :return:
        """
        try:
            logger.info('bulk executeSql starts')

            # Create connection instance
            connection_pool = Mysql.getConnectionPool(self.db)
            conn = connection_pool.get_connection()

            # Create a cursor instance
            cursor = conn.cursor(dictionary=True, buffered=True)

            try:
                # Bulk insert using executemany
                cursor.executemany(sql, data)

                # Commit
                conn.commit()

                # Close cursor, connection close
                self.__close(conn, cursor)

                logger.info('bulk executeSql ends')

            # Exception occurs when fetchall insert result
            except BaseException:
                # Commit
                conn.commit()

                # Close cursor, connection close
                self.__close(conn, cursor)

                logger.info('executeSql ends')
                pass

    def execute_sql(self, sql, bindings=None):
        """
        :param sql:
        :param bindings:
        :return:
        """
        try:
            logger.info('executeSql starts')

            # Create connection instance
            connection_pool = Mysql.getConnectionPool(self.db)
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
                self.__close(conn, cursor)

                logger.info('executeSql ends')

                return sql_result

            # Exception occurs when fetchall insert result
            except BaseException:
                # Commit
                conn.commit()

                # Close cursor, connection close
                self.__close(conn, cursor)

                logger.info('executeSql ends')
                pass

        except Exception as e:
            conn.rollback()

            # Close cursor, connection close
            self.__close(conn, cursor)

            raise e

    def __close(self, conn, cursor):
        try:
            # Close cursor, connection close
            cursor.close()
            logger.info('cursor closed')

            conn.close()
            logger.info('connection closed')

        except Exception as e:
            raise e
