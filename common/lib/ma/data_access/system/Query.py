class Query():
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

    sql_select_status_in_60_min = """
        SELECT *
        FROM contact_status
        WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) <= 60;
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
        SELECT m.gmail_thread_id, m.gmail_msg_id, m.t_key, i.receiver_email, i.tiktok_url, m.created_at
        FROM (
            SELECT DISTINCT gmail_thread_id, gmail_msg_id, t_key, created_at
            FROM mail_contact t1
            WHERE NOT EXISTS (
                SELECT 1
                FROM mail_contact t2
                WHERE t2.gmail_thread_id = t1.gmail_thread_id
                AND t2.gmail_label_id = 'INBOX'
            )
        ) m
        JOIN infl_contact_info_master i ON m.t_key = i.t_key
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

    sql_update_mail_contact_thread_id = """
        UPDATE mail_contact SET gmail_thread_id = '{new_gmail_thread_id}', gmail_msg_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """

    sql_update_contact_status_thread_id = """
        UPDATE contact_status SET gmail_thread_id = '{new_gmail_thread_id}'
        WHERE gmail_thread_id = '{old_gmail_thread_id}'
    """