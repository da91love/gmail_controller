import logging
from psycopg2.extras import DictCursor

# call instancese
logger = logging.getLogger()

"""
executeSelect function
    :param conn: database connection instance
    :param sql: string
    :param binding: tuple
    :return: tuple. sql result
"""


def executeSql(conn, sql, is_column=None, bindings=None):
    try:
        logger.info('executeSql starts')
        # Create a cursor instance
        if is_column:
            cursor = conn.cursor(cursor_factory=DictCursor)
        else:
            cursor = conn.cursor()

        if bindings:
            sql = sql.format(**bindings)

        logger.info(sql)
        cursor.execute(sql)

        # Commit
        conn.commit()

        try:
            psql_result = cursor.fetchall()
            logger.info('executeSql ends')

            if is_column:
                dict_result = []
                for row in psql_result:
                    dict_result.append(dict(row))
                return dict_result
            else:
                return psql_result
        except BaseException:
            logger.info('executeSql ends')
            pass

    except Exception as e:
        conn.rollback()
        raise e
