class Query():
    sql_select_is_in_process_history = """
        SELECT slack_post_block_id FROM operation_process
        WHERE export_id = '{export_id}' and delivery_type = '{delivery_type}' and slack_post_block_id is not null;
    """

    sql_insert_op_process = """
        insert into operation_process (export_id, delivery_type, doc_type, requester, slack_post_block_id) 
        values ('{export_id}', '{delivery_type}', '{doc_type}','{requester}','{slack_post_block_id}')
    """

    sql_truncate_invoice_master = """
        TRUNCATE invoice_master
    """

    sql_insert_invoice_master = """
        INSERT INTO invoice_master (export_no, customer, product_name, country, product_code, quantity, currency, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    sql_update_slack_history = """
        update slack_thread_history set 
            pic='{pic}',
            requester='{requester}',
            brand='{brand}',
            export_id='{export_id}', 
            buyer_name='{buyer_name}', 
            address='{address}', 
            recipient='{recipient}', 
            recipient_phone_num='{recipient_phone_num}', 
            requested_arrival_date='{requested_arrival_date}', 
            bill_type='{bill_type}', 
            folder_id='{folder_id}', 
            delivery='{delivery}',
            delivery_type='{delivery_type}',
            remark='{remark}',
            updated_at=NOW() 
        where export_id='{export_id}' and slack_post_block_id='{slack_post_block_id}';
    """

    sql_insert_slack_history = """
        insert into slack_thread_history (export_id, slack_post_block_id, pic, requester, brand, buyer_name, address, recipient, recipient_phone_num, requested_arrival_date, bill_type, folder_id, delivery, delivery_type, remark) 
        values ('{export_id}','{slack_post_block_id}','{pic}', '{requester}', '{brand}','{buyer_name}','{address}','{recipient}','{recipient_phone_num}','{requested_arrival_date}','{bill_type}','{folder_id}','{delivery}','{delivery_type}','{remark}')
    """

    sql_select_slack_history = """
        SELECT *
        FROM slack_thread_history
        WHERE export_id = '{export_id}' and delivery_type = '{delivery_type}';
    """

    sql_delete_temp = """
        DELETE FROM contact_status where gmail_thread_id='{old_gmail_thread_id}';
    """

    sql_select_all_orders = """
        SELECT amazon_order_id, real_purchase_date, address_json
        FROM amazon_seller_report_order_infos asro
        LEFT JOIN amazon_seller_report_order_detail_infos asr on asr.amazon_seller_report_order_info_id = asro.id
        WHERE marketplaceid = 'ATVPDKIKX0DER'
          AND asin = 'B0CMC6S4BM'
          AND item_price > 0
          AND '{start_date}' <= real_purchase_date
        AND real_purchase_date < '{end_date}'
        ORDER BY real_purchase_date desc
    """

    sql_select_spark_ads_trk_tg = """
        SELECT pim.*
        FROM (
            select * from sa_payment_info_master
            where spark_ads_start_date <= CURDATE() and CURDATE() < spark_ads_end_date
        ) spim
        LEFT JOIN post_info_master pim ON pim.post_id = spim.post_id
    """

    insert_clm_posting_history="""
        INSERT INTO clm_posting_history(tg_date, this_week_post_num, this_week_view_count, last_week_post_num, last_week_view_count) 
        VALUES('{tg_date}', '{this_week_post_num}','{this_week_view_count}','{last_week_post_num}','{last_week_view_count}')
    """

    sql_select_posting_history_in_day = """
        select *
        from posting_history
        where '{from_date}' <= posted_time and posted_time < '{to_date}'
    """

    sql_select_today_post = """
        select *
        from post_info_master
        where posting_date = '{today}'
    """

    sql_select_sent_mail_contact = """
        select *
        from (
              SELECT
                t_key,
                created_at,
                COUNT(CASE WHEN gmail_label_id = 'SENT' THEN 1 END) AS SENT_count,
                COUNT(CASE WHEN gmail_label_id = 'INBOX' THEN 1 END) AS INBOX_count
              FROM mail_contact
              GROUP BY
                t_key
        ) s
        where s.SENT_count=1 and s.INBOX_count=0 and s.created_at >= '{today}'
    """

    sql_select_keyword_master = """
        select * from keyword_master
    """

    sql_select_delivery_info_master = """
        select * from delivery_info_master where issue_date='{today}'
    """

    sql_select_today_contacts = """
        select *
        from (
            select k.t_key, md.sender_email, k.SENT_count, k.INBOX_count
            from (
                select icim.t_key, icim.sender_email
                from (
                    select t_key
                    from mail_contact mc
                    where created_at >= '{today}' and gmail_label_id='SENT'
                ) mc
                join infl_contact_info_master icim on icim.t_key = mc.t_key
            ) md
            join (
                SELECT
                    mc.t_key,
                    COUNT(CASE WHEN mc.gmail_label_id = 'SENT' THEN 1 END) AS SENT_count,
                    COUNT(CASE WHEN mc.gmail_label_id = 'INBOX' THEN 1 END) AS INBOX_count
                FROM mail_contact mc
                GROUP BY
                    mc.gmail_thread_id
            ) k on k.t_key = md.t_key
        ) aa
        where aa.INBOX_count > 0 and aa.sender_email='{sender_email}'
    """

    sql_select_pic_email_match="""
        SELECT * FROM pic_email_match
    """

    sql_insert_pic="""
        INSERT INTO person_in_charge(t_key, pic) 
        VALUES('{t_key}','{pic}')
    """

    sql_insert_infl_contact_info="""
        INSERT INTO infl_contact_info_master(t_key, author_unique_id, seeding_num, tg_brand, channel, tg_country, receiver_email, tiktok_url, source_type, sender_email) 
        VALUES('{t_key}','{author_unique_id}','{seeding_num}','{tg_brand}','{channel}', '{tg_country}', '{receiver_email}', '{tiktok_url}', '{source_type}', '{sender_email}')
    """

    sql_select_mia= """
        select *
        from (
            select mc.*, ici.author_unique_id, ici.receiver_email, ici.sender_email, ici.tiktok_url, pic.pic, cs.status, cs.progress
            from mail_contact mc
            join contact_status cs on cs.t_key = mc.t_key
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
        JOIN contact_status cs ON cs.t_key = mc.t_key
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
        join person_in_charge pi on pi.t_key = m.t_key
        ORDER BY m.id ASC
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
        WHERE t_key='{t_key}'
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
        INSERT INTO slack_thread_history(slack_thread_id, t_key, gmail_msg_id, created_at) 
        VALUES('{slack_thread_id}', '{t_key}', '{gmail_msg_id}', '{created_at}')
    """

    # INBOX 라벨이 붙지않은 메일 스레드
    sql_select_sent_thread_id = """
        SELECT m.gmail_thread_id, m.gmail_msg_id, m.t_key, i.receiver_email, i.sender_email, i.add_to_sys, i.tiktok_url, cs.status, cs.progress, pi.pic, m.created_at
        FROM (
			SELECT DISTINCT t1.*
			FROM mail_contact t1
			LEFT JOIN mail_contact t2 ON t1.gmail_thread_id = t2.gmail_thread_id AND t2.gmail_label_id = 'INBOX'
			WHERE t2.gmail_label_id IS NULL
		) m
        JOIN infl_contact_info_master i ON m.t_key = i.t_key
        JOIN contact_status cs ON cs.t_key = m.t_key
        JOIN person_in_charge pi ON pi.t_key = m.t_key
        WHERE m.created_at > '2024-03-11'
    """

    sql_select_mail_contact_by_gti = """
        SELECT * FROM mail_contact
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_select_mail_contact_by_tkey = """
        SELECT * FROM mail_contact
        WHERE t_key='{t_key}'
    """

    sql_insert_contents = """
        INSERT INTO mail_contents(gmail_thread_id, gmail_msg_id, contents, created_at) 
        VALUES('{gmail_thread_id}', '{gmail_msg_id}', '{contents}', '{created_at}')
    """

    sql_select_contacts_status = """
        SELECT * FROM contact_status
        WHERE t_key='{t_key}'
    """

    sql_insert_contact_status = """
        INSERT INTO contact_status(t_key, status, progress) 
        VALUES('{t_key}', '{status}', '{progress}')
    """

    sql_insert_contact_history = """
        INSERT INTO mail_contact(gmail_thread_id, gmail_msg_id, gmail_label_id, t_key, created_at) 
        VALUES('{gmail_thread_id}', '{gmail_msg_id}', '{gmail_label_id}', '{t_key}', '{created_at}')
    """

    sql_insert_infl_info = """
        INSERT INTO infl_info(gmail_thread_id, author_unique_id, receiver_email, tiktok_url) 
        VALUES('{gmail_thread_id}', '{author_unique_id}', '{receiver_email}', '{tiktok_url}')
    """

