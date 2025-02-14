from common.lib.ma.data_access.AccessServiceBase import AccessServiceBase
# from common.lib.i18n.i18n import I18n
from .Query import Query


class AccessService():

    def __init__(self, db):
        self.db = db
    
    """
    All function's name should start with below 4 verbs: select insert update delete
    """
    def update_slack_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_update_slack_history,
                bindings=bindings)

        except Exception as e:
            raise e

    def insert_slack_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_slack_history,
                bindings=bindings)

        except Exception as e:
            raise e

    def select_slack_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_slack_history,
                bindings=bindings)

        except Exception as e:
            raise e

    def select_all_orders(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_all_orders,
                bindings=bindings)

        except Exception as e:
            raise e


    def select_spark_ads_trk_tg(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_spark_ads_trk_tg,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_clm_posting_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """

        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.insert_clm_posting_history,
                bindings=bindings)

        except Exception as e:
            raise e

    def select_posting_history_in_day(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_posting_history_in_day,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_today_post(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_today_post,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_sent_mail_contact(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_sent_mail_contact,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_keyword_master(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_keyword_master,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_delivery_info_master(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_delivery_info_master,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_today_contacts(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_today_contacts,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_pic_email_match(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_pic_email_match,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_pic(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_pic,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_infl_contact_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_infl_contact_info,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_mia(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_mia,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_follow_up_check(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_follow_up_check,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_follow_up_mail_info_by_tkey(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_follow_up_mail_info_by_tkey,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_follow_up_by_thread(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_follow_up_by_thread,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_follow_up_tg_list(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_follow_up_tg_list,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def insert_profile_stats(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_profile_stats,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_mega_posting_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_mega_posting_history,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_posting_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_posting_history,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_mega_posting_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_mega_posting_history,
                bindings=bindings)

        except Exception as e:
            raise e
    def insert_posting_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_posting_history,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_mega_post_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_mega_post_info,
                bindings=bindings)

        except Exception as e:
            raise e
    def select_post_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_post_info,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_infl_info_by_email(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_infl_info_by_email,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def delete_temp_status(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_delete_temp,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_temp(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_temp,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def update_gmail_mail_contents_thread_id(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_update_mail_contents_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def update_delivery_master(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_update_delivery_master,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def update_gmail_mail_contact_thread_id(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_update_mail_contact_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_latest_thread_id_by_tkey(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_latest_thread_id_by_tkey,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_contact_num_by_tkey(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_contact_num_by_tkey,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_past_on_contact_infl(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_past_on_contact_infl,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_infl_first_contact(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_infl_first_contact,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_delivery_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_delivery_history,
                bindings=bindings)

        except Exception as e:
            raise e


    
    def insert_delivery_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_delivery_history,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_delivery_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_delivery_info,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_infl_contact_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_infl_contact_info,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_thread_id_by_email(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_thread_id_by_email,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_status_in_x_min(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_status_in_x_min,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_pic(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_pic,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def select_slack_thread_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_slack_thread_history,
                bindings=bindings)

        except Exception as e:
            raise e


    
    def select_slack_need_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_slack_need_info,
                bindings=bindings)

        except Exception as e:
            raise e
    
    def insert_slack_thread_id(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_slack_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_sent_thread_id(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_sent_thread_id,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_contacts_by_gti(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_mail_contact_by_gti,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_contacts_by_tkey(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_mail_contact_by_tkey,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_contents(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_contents,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def select_contacts_status(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_select_contacts_status,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_contact_status(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_contact_status,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_contact_history(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_contact_history,
                bindings=bindings)

        except Exception as e:
            raise e

    
    def insert_infl_info(self, **bindings):
        """
        :param bindings: (tuple)
        :return: (list) sql query result
        """
        try:
            return AccessServiceBase(self.db).execute_sql(
                sql=Query.sql_insert_infl_info,
                bindings=bindings)

        except Exception as e:
            raise e