class Query():

    sql_select_thread_id_by_email = """
    SELECT mc.gmail_thread_id, mc.author_unique_id, mc.seeding_num, mc.tg_brand, latest_emails.receiver_email
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
    ON mc.author_unique_id = latest_emails.author_unique_id
        AND mc.seeding_num = latest_emails.seeding_num
        AND mc.tg_brand = latest_emails.tg_brand
    WHERE latest_emails.receiver_email = '{receiver_email}'
    """

    sql_select_status_in_10_min = """
        SELECT *
        FROM contact_status
        WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) <= 10;
    """

    sql_select_pic = """
        SELECT * FROM person_in_charge
        WHERE author_unique_id='{author_unique_id}' and seeding_num='{seeding_num}' and tg_brand='{tg_brand}'
    """

    sql_select_slack_thread_history = """
        SELECT * FROM slack_thread_history
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_select_slack_need_info = """           
        SELECT 
            mc.author_unique_id,
            ici.receiver_email,
            ici.tiktok_url,
            pic.pic
        FROM 
            mail_contact mc
        INNER JOIN 
            infl_contact_info_master ici ON mc.author_unique_id = ici.author_unique_id
                                        AND mc.seeding_num = ici.seeding_num
                                        AND mc.tg_brand = ici.tg_brand
        INNER JOIN 
            person_in_charge pic ON mc.author_unique_id = pic.author_unique_id
                                  AND mc.seeding_num = pic.seeding_num
                                  AND mc.tg_brand = pic.tg_brand
        WHERE 
            mc.author_unique_id = '{author_unique_id}'
            AND mc.seeding_num = {seeding_num}
            AND mc.tg_brand = '{tg_brand}'
        GROUP BY
          gmail_thread_id;    
    """

    sql_insert_slack_thread_id = """
        INSERT INTO slack_thread_history(slack_thread_id, gmail_thread_id, gmail_msg_id, created_at) 
        VALUES('{slack_thread_id}', '{gmail_thread_id}', '{gmail_msg_id}', '{created_at}')
    """

    # INBOX 라벨이 붙지않은 메일 스레드
    sql_select_sent_thread_id = """
        SELECT m.gmail_thread_id, m.gmail_msg_id, m.author_unique_id, m.seeding_num, m.tg_brand, i.receiver_email, i.tiktok_url, m.created_at
        FROM (
            SELECT DISTINCT gmail_thread_id, gmail_msg_id, author_unique_id, seeding_num, tg_brand, created_at
            FROM mail_contact t1
            WHERE NOT EXISTS (
                SELECT 1
                FROM mail_contact t2
                WHERE t2.gmail_thread_id = t1.gmail_thread_id
                AND t2.gmail_label_id = 'INBOX'
            )
        ) m
        JOIN infl_contact_info_master i ON m.author_unique_id = i.author_unique_id AND m.seeding_num = i.seeding_num
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
        INSERT INTO mail_contact(gmail_thread_id, gmail_msg_id, gmail_label_id, author_unique_id, seeding_num, tg_brand, created_at) 
        VALUES('{gmail_thread_id}', '{gmail_msg_id}', '{gmail_label_id}', '{author_unique_id}', '{seeding_num}', '{tg_brand}', '{created_at}')
    """

    sql_insert_infl_info = """
        INSERT INTO infl_info(gmail_thread_id, author_unique_id, receiver_email, tiktok_url) 
        VALUES('{gmail_thread_id}', '{author_unique_id}', '{receiver_email}', '{tiktok_url}')
    """

    sql_update_mail_contact_thread_id = """
        UPDATE mail_contact SET gmail_thread_id = '{new_gmail_thread_id}', gmail_msg_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """

    sql_update_contact_status_thread_id = """
        UPDATE contact_status SET gmail_thread_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """