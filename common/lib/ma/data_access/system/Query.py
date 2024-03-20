class Query():
    sql_delete_temp = """
        DELETE FROM contact_status where gmail_thread_id='{old_gmail_thread_id}';
    """

    sql_temp = """
        SELECT * FROM mail_contact 
    """

    sql_select_mia= """
        select *
        from (
            select mc.*, ici.author_unique_id, ici.receiver_email, ici.sender_email, ici.tiktok_url, pic.pic, cs.status, cs.progress
            from mail_contact mc
            join contact_status cs on cs.gmail_thread_id = mc.gmail_thread_id
            join infl_contact_info_master ici on ici.t_key = mc.t_key
            join person_in_charge pic on pic.t_key = mc.t_key
        ) tg
        where tg.status = 'open' and tg.progress <> 'deal_finish'
    """

    sql_insert_follow_up_check = """
        INSERT INTO follow_up_check (t_key, is_follow_up_done) 
        VALUES('{t_key}', true)
    """

    sql_select_follow_up_mail_info_by_tkey = """
        select mc.gmail_thread_id, ici.receiver_email, ici.sender_email
        from mail_contact mc
        join infl_contact_info_master ici on ici.t_key = mc.t_key
        where mc.t_key='{t_key}'
        group by mc.gmail_thread_id
    """

    sql_select_follow_up_by_thread = """
        SELECT * FROM follow_up_check
        WHERE t_key = '{t_key}'
    """

    sql_select_follow_up_tg_list = """
        select pim.post_id, pim.t_key, pim.seeding_source_type, pim.tiktok_url, ph.posted_time
        from post_info_master pim
        join posting_history ph on ph.post_id = pim.post_id
        where pim.seeding_source_type = 'bsts'
        group by pim.post_id
    """

    sql_insert_profile_stats = """
        INSERT INTO tiktok_profile_stat(id, author_unique_id, digg_count, follower_count, following_count, friend_count, heart, heart_count, video_count) 
        VALUES('{id}','{author_unique_id}','{digg_count}','{follower_count}', '{following_count}', '{friend_count}', '{heart}', '{heart_count}', '{video_count}')
    """

    sql_select_mega_posting_history = """
        SELECT * FROM mega_posting_history
    """

    sql_select_posting_history = """
        SELECT * FROM posting_history
    """

    sql_insert_mega_posting_history = """
        INSERT INTO mega_posting_history (post_id, posted_time, collect_count, comment_count, digg_count, play_count, share_count, tags) 
        VALUES('{post_id}', '{posted_time}', '{collect_count}', '{comment_count}', '{digg_count}', '{play_count}', '{share_count}', '{tags}')
    """

    sql_insert_posting_history = """
        INSERT INTO posting_history (post_id, posted_time, collect_count, comment_count, digg_count, play_count, share_count, tags) 
        VALUES('{post_id}', '{posted_time}', '{collect_count}', '{comment_count}', '{digg_count}', '{play_count}', '{share_count}', '{tags}')
    """

    sql_select_post_info = """
        SELECT * FROM post_info_master
    """

    sql_select_mega_post_info = """
        SELECT * FROM mega_post_info_master
    """


    sql_select_infl_info_by_email = """
        SELECT *
        FROM infl_contact_info_master
        WHERE receiver_email = '{receiver_email}'
    """

    sql_update_mail_contents_thread_id = """
        UPDATE mail_contents SET gmail_thread_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """

    sql_update_mail_contact_thread_id = """
        UPDATE mail_contact SET gmail_thread_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """
    # sql_update_mail_contact_thread_id = """
    #     UPDATE mail_contact SET gmail_thread_id = '{new_gmail_thread_id}', gmail_msg_id = '{new_gmail_thread_id}'
    #     WHERE gmail_thread_id = '{old_gmail_thread_id}'
    # """

    sql_update_contact_status_thread_id = """
        UPDATE contact_status SET gmail_thread_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """

    sql_update_slack_thread_id = """
        UPDATE slack_thread_history SET gmail_thread_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """

    sql_update_delivery_master = """
        UPDATE delivery_info_master SET delivery_status = '{delivery_status}'
        WHERE order_id = '{order_id}' AND invoice_id = '{invoice_id}';
    """

    sql_select_latest_thread_id_by_tkey= """
        SELECT t1.t_key, t1.gmail_thread_id
        FROM mail_contact t1
        JOIN (
            SELECT t_key, MAX(created_at) AS max_created_at
            FROM mail_contact
            GROUP BY t_key
        ) t2 ON t1.t_key = t2.t_key AND t1.created_at = t2.max_created_at
    """

    sql_select_contact_num_by_tkey= """
        SELECT
            t_key,
            COUNT(DISTINCT gmail_thread_id) AS thread_count
        FROM mail_contact
        GROUP BY t_key;
    """

    sql_select_past_on_contact_infl= """
        SELECT mc.t_key, ic.author_unique_id, ic.receiver_email, ic.sender_email, pic.pic
        FROM (
            SELECT *
            FROM mail_contact
            WHERE gmail_label_id = 'INBOX' AND created_at < '{tg_date}'
            GROUP BY gmail_thread_id
        ) mc
        JOIN contact_status cs ON cs.gmail_thread_id = mc.gmail_thread_id
        JOIN infl_contact_info_master ic ON ic.t_key = mc.t_key
        JOIN person_in_charge pic ON pic.t_key = mc.t_key
        WHERE cs.status = 'open'
    """

    sql_select_infl_first_contact= """
        SELECT m.*, pi.pic
        FROM (
            SELECT *
            FROM infl_contact_info_master
            WHERE t_key NOT IN (SELECT DISTINCT t_key FROM mail_contact)
        ) m
        join person_in_charge pi on pi.t_key = m.t_key;
    """

    sql_select_delivery_history = """
        SELECT *
        FROM delivery_tracking_history
        WHERE invoice_id = '{invoice_id}'
    """

    sql_insert_delivery_history = """
        INSERT INTO delivery_tracking_history (order_id, invoice_id, delivery_status, event_time) 
        VALUES('{order_id}', '{invoice_id}', '{delivery_status}', '{event_time}')
    """

    sql_select_delivery_info = """
        SELECT order_id, invoice_id, courier
        FROM delivery_info_master
        WHERE delivery_status != 'Delivered'
    """

    sql_select_infl_contact_info = """
        SELECT *
        FROM infl_contact_info_master
        WHERE t_key = '{t_key}'
    """

    sql_select_thread_id_by_email = """
    SELECT mc.gmail_thread_id, mc.t_key, latest_emails.receiver_email
    FROM mail_contact mc
    JOIN (
            SELECT *
            FROM infl_contact_info_master
            WHERE (receiver_email, created_at) IN (
                SELECT receiver_email, MAX(created_at)
                FROM infl_contact_info_master
                GROUP BY receiver_email
            )
    ) AS latest_emails
    ON mc.t_key = latest_emails.t_key
    WHERE latest_emails.receiver_email = '{receiver_email}'
    """

    sql_select_status_in_x_min = """
        SELECT *
        FROM contact_status
        WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) <= 200;
    """

    sql_select_pic = """
        SELECT * FROM person_in_charge
        WHERE t_key='{t_key}'
    """

    sql_select_slack_thread_history = """
        SELECT * FROM slack_thread_history
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_select_slack_need_info = """
        SELECT 
            mc.t_key,
            ici.author_unique_id,
            ici.receiver_email,
            ici.sender_email,
            ici.tiktok_url,
            pic.pic
        FROM 
            mail_contact mc
        INNER JOIN 
            infl_contact_info_master ici ON mc.t_key = ici.t_key
        INNER JOIN 
            person_in_charge pic ON mc.t_key = pic.t_key
        WHERE 
            mc.t_key = '{t_key}'
        GROUP BY
          gmail_thread_id   
    """

    sql_insert_slack_thread_id = """
        INSERT INTO slack_thread_history(slack_thread_id, gmail_thread_id, gmail_msg_id, created_at) 
        VALUES('{slack_thread_id}', '{gmail_thread_id}', '{gmail_msg_id}', '{created_at}')
    """

    # INBOX 라벨이 붙지않은 메일 스레드
    sql_select_sent_thread_id = """
        SELECT m.gmail_thread_id, m.gmail_msg_id, m.t_key, i.receiver_email, i.sender_email, i.tiktok_url, cs.status, cs.progress, pi.pic, m.created_at
        FROM (
			SELECT DISTINCT t1.*
			FROM mail_contact t1
			LEFT JOIN mail_contact t2 ON t1.gmail_thread_id = t2.gmail_thread_id AND t2.gmail_label_id = 'INBOX'
			WHERE t2.gmail_label_id IS NULL
		) m
        JOIN infl_contact_info_master i ON m.t_key = i.t_key
        JOIN contact_status cs ON cs.gmail_thread_id = m.gmail_thread_id
        JOIN person_in_charge pi ON pi.t_key = m.t_key
        WHERE m.created_at > '2024-03-11'
    """

    sql_select_mail_contact = """
        SELECT * FROM mail_contact
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_insert_contents = """
        INSERT INTO mail_contents(gmail_thread_id, gmail_msg_id, contents, created_at) 
        VALUES('{gmail_thread_id}', '{gmail_msg_id}', '{contents}', '{created_at}')
    """

    sql_select_contacts_status = """
        SELECT * FROM contact_status
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_insert_contact_status = """
        INSERT INTO contact_status(gmail_thread_id, status, progress) 
        VALUES('{gmail_thread_id}', '{status}', '{progress}')
    """

    sql_insert_contact_history = """
        INSERT INTO mail_contact(gmail_thread_id, gmail_msg_id, gmail_label_id, t_key, created_at) 
        VALUES('{gmail_thread_id}', '{gmail_msg_id}', '{gmail_label_id}', '{t_key}', '{created_at}')
    """

    sql_insert_infl_info = """
        INSERT INTO infl_info(gmail_thread_id, author_unique_id, receiver_email, tiktok_url) 
        VALUES('{gmail_thread_id}', '{author_unique_id}', '{receiver_email}', '{tiktok_url}')
    """

