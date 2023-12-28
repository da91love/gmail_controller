from common.lib.ma.data_access.AccessServiceBase import AccessServiceBase
# from common.lib.i18n.i18n import I18n
from .Query import Query


class AccessService(AccessServiceBase):

    """
    All function's name should start with below 4 verbs: select insert update delete
    """
    @staticmethod
    def select_pic(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_pic,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def select_slack_thread_history(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_slack_thread_history,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def select_infl_info(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_infl_info,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def insert_slack_thread_id(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_insert_slack_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def select_sent_thread_id(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_sent_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def select_contact_num(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_contact_num,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def insert_contents(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_insert_contents,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def insert_contact_history(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_insert_contact_history,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def insert_infl_info(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_insert_infl_info,
                bindings=bindings)

        except Exception as e:
            raise e