from common.lib.ma.data_access.AccessServiceBase import AccessServiceBase
# from common.lib.i18n.i18n import I18n
from .Query import Query


class AccessService(AccessServiceBase):

    """
    All function's name should start with below 4 verbs: select insert update delete
    """
    @staticmethod
    def select_contact_num_by_tkey(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.select_contact_num_by_tkey,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def select_past_on_contact_infl(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.select_past_on_contact_infl,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def select_infl_first_contact(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_infl_first_contact,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def select_delivery_history(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_delivery_history,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def update_delivery_master(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_update_delivery_master,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def insert_delivery_history(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_insert_delivery_history,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def select_delivery_info(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_delivery_info,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def select_infl_contact_info(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_infl_contact_info,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def select_thread_id_by_email(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_thread_id_by_email,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def update_gmail_contact_status_thread_id(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_update_contact_status_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def update_gmail_mail_contact_thread_id(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_update_mail_contact_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e
    @staticmethod
    def select_status_in_x_min(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_status_in_x_min,
                bindings=bindings)

        except Exception as e:
            raise e

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
    def select_slack_need_info(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_slack_need_info,
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
    def select_contacts(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_mail_contact,
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
    def select_contacts_status(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_select_contacts_status,
                bindings=bindings)

        except Exception as e:
            raise e

    @staticmethod
    def insert_contact_status(**bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase.execute_sql(
                sql=Query.sql_insert_contact_status,
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