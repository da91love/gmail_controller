class Query():
    sql_select_pic = """
        SELECT * FROM person_in_charge
        WHERE author_unique_id='{author_unique_id}' and seeding_num='{seeding_num}'
    """

    sql_select_slack_thread_history = """
        SELECT * FROM slack_thread_history
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_select_slack_need_info = """
        SELECT tiktok_url, receiver_email, gmail_msg_id
        FROM infl_contact_info_master
        INNER JOIN mail_contact ON
            infl_contact_info_master.author_unique_id = mail_contact.author_unique_id
            AND infl_contact_info_master.seeding_num = mail_contact.seeding_num
        WHERE infl_contact_info_master.author_unique_id = '{author_unique_id}'
            AND infl_contact_info_master.seeding_num = {seeding_num};
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

    sql_select_contact_num = """
        SELECT * FROM mail_contact
        WHERE gmail_thread_id='{gmail_thread_id}'
    """

    sql_insert_contents = """
        INSERT INTO mail_contents(gmail_thread_id, gmail_msg_id, contents, created_at) 
        VALUES('{gmail_thread_id}', '{gmail_msg_id}', '{contents}', '{created_at}')
    """

    sql_select_contact_status = """
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


    sql_insert_comp_tg_grp = """
        INSERT INTO compare_tg_group(user_id, value) 
        VALUES('{user_id}', '{value}')
        ON DUPLICATE KEY UPDATE value = '{value}', updated_at = CURRENT_TIMESTAMP
    """


    sql_select_comp_tg_grp = """
        SELECT * FROM compare_tg_group
        WHERE user_id='{user_id}'
    """

    sql_insert_valuation = """
        INSERT INTO valuation_value(user_id, value) 
        VALUES('{user_id}', '{value}')
        ON DUPLICATE KEY UPDATE value = '{value}', updated_at = CURRENT_TIMESTAMP
    """

    sql_select_valuation = """
        SELECT * FROM valuation_value
        WHERE user_id='{user_id}'
    """

    sql_select_bookmark = """
        SELECT * FROM bookmarked_share
        WHERE user_id='{user_id}'
    """

    sql_insert_bookmark = """
        INSERT INTO bookmarked_share(user_id, value) 
        VALUES('{user_id}', '{value}')
        ON DUPLICATE KEY UPDATE value = '{value}', updated_at = CURRENT_TIMESTAMP
    """

    sql_select_auth_id = """
        SELECT * FROM user_auth_id WHERE auth_id='{auth_id}'
    """

    sql_delete_auth_id = """
        DELETE FROM user_auth_id
        WHERE user_id='{user_id}'
    """

    sql_insert_auth_id = """
        INSERT INTO user_auth_id(user_id, auth_id) 
        VALUES('{user_id}', '{auth_id}')
    """

    sql_select_user_id_pw = """
        SELECT * FROM user_id_pw
        WHERE user_id='{user_id}'
    """


    test = """
     	    with crt_item as (
                select *
                from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_created_at
                    FROM core_engine_test.item_current_model) as s
                where created_at=max_created_at and item_key='{item_key}'
            ),
            smlts_by_item as (
                select item_smlt.*
                from core_engine_test.item_simulation as item_smlt
                    join crt_item
                        on crt_item.item_key = item_smlt.item_key
    					and crt_item.model_cd = item_smlt.model_cd
            ),
            crt_smlt_by_item as (
                select max_created_at_by_item_key.*
                from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_created_at
                    FROM smlts_by_item) as max_created_at_by_item_key
                where created_at=max_created_at
            )

            select crt_smlt_by_item.item_key,
                    crt_smlt_by_item.model_cd,
                    crt_smlt_by_item.simulation_key
            from crt_smlt_by_item
        """

    sql_select_crt_smlt = """
 	    with crt_item as (
            select *
            from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_created_at
                FROM core_engine_test.item_current_model) as s
            where created_at=max_created_at and item_key='{item_key}'
        ),
        smlts_by_item as (
            select item_smlt.*
            from core_engine_test.item_simulation as item_smlt
                join crt_item
                    on crt_item.item_key = item_smlt.item_key
					and crt_item.model_cd = item_smlt.model_cd
        ),
        crt_smlt_by_item as (
            select max_created_at_by_item_key.*
            from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_created_at
                FROM smlts_by_item) as max_created_at_by_item_key
            where created_at=max_created_at
        )

        select crt_smlt_by_item.item_key,
                crt_smlt_by_item.model_cd,
                crt_smlt_by_item.simulation_key
        from crt_smlt_by_item
    """

    sql_select_simulation = """
        with item_model_map as (
            select model_map.item_key, model_map.model_cd,m_model.engine_cd,m_model.engine_version,m_model.candidate_group_cd
            from core_engine_test.item_model_map as model_map
			left outer join core_engine_test.m_model as m_model
			on model_map.model_cd = m_model.model_cd
            where item_key = '{item_key}'
        ),
        item_simulation as (
            select simulation_key,item_key,model_cd,period_from,period_to
            from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key, model_cd) as max_created_at
                FROM core_engine_test.item_simulation) as s
            where created_at=max_created_at and item_key='{item_key}'
        ),
        /*m_itemはclosing_dayをjoinするため*/
        m_item as (
            select item_key, closing_day
            from core_engine_test.m_item
            where item_key='{item_key}'
        ),
        /*item_crt_mdlは最新のitem modelをjoinするため*/
        item_current_model as (
            select item_key,model_cd, 1 as crt_mdl_flg
                from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_time
                    FROM core_engine_test.item_current_model) as s
            where created_at=max_time and item_key='{item_key}'
        ),
        /*item_crt_smltは最新のitem simulationをjoinするため*/
        item_current_simulation as (
            select item_key,simulation_key,simulation_type, 1 as crt_smlt_flg
            from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_time
            FROM core_engine_test.item_current_simulation) as s
            where created_at=max_time and item_key='{item_key}'
        ),
		mdl_grp as (
			select model_group_cd, model_cd
			from core_engine_test.m_model_group
		)

		select
			main.item_key,
			mdl_grp.model_group_cd,
			mdl_grp.model_cd,
			main.candidate_group_cd,
			item_simulation.simulation_key,
			item_simulation.period_from as busidate,
			m_item.closing_day,
			COALESCE(item_current_model.crt_mdl_flg, 0) as crt_mdl_flg,
			COALESCE(item_current_simulation.crt_smlt_flg, 0) as crt_smlt_flg
		from item_model_map as main
			left outer join item_simulation
				on main.item_key = item_simulation.item_key
					and main.model_cd = item_simulation.model_cd
			left outer join m_item
				on main.item_key = m_item.item_key
			left outer join item_current_model
				on main.item_key = item_current_model.item_key
					and main.model_cd  = item_current_model.model_cd
			left outer join item_current_simulation
				on main.item_key = item_current_simulation.item_key
					and item_simulation.simulation_key = item_current_simulation.simulation_key
			join mdl_grp
				on mdl_grp.model_cd = main.model_cd
		where item_simulation.period_from = '{busidate}'
    """

    sql_select_item_crt_smlt_analysis = """
	    with
	    /* model_group_cdで絞るため  */
        mdl_grp as (
			select model_group_cd, model_cd
			from core_engine_test.m_model_group
			where model_group_cd='{model_group_cd}'
		),
		/* 特定item_key, busidateの最新item_simulationデータ  */
        lst_sml as (
			select *
			from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key, model_cd) as max_time
								FROM core_engine_test.item_simulation) as his
			where created_at=max_time and item_key='{item_key}' and period_from = '{busidate}'
        ),
		/* engine_cd, engine_version, candidate_group_cdをjoinするため  */
		mdl as (
			select *
			from core_engine_test.m_model
		),
		/* model_group_cdで絞ったmodel_cdでlst_icm結果を絞る  */
		lst_sml_by_mdl as (
			select lst_sml.*, mdl.engine_cd, mdl.engine_version, mdl.candidate_group_cd
			from lst_sml
			inner join mdl_grp
				on mdl_grp.model_cd = lst_sml.model_cd
			join mdl
				on mdl.model_cd = lst_sml.model_cd
		),
		/* 特定item_keyの最新item_current_modelデータ：Modal画面で選ばれているデータ  */
		lst_icm as (
			select *
			from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_time
								FROM core_engine_test.item_current_simulation) as his
			where created_at=max_time and item_key='{item_key}'
		)

        select '{s3_bucket_name}' as s3_bucket_name,
               lst_sml_by_mdl.engine_cd ||
               '/' || lst_sml_by_mdl.engine_version ||
               '/' || lst_sml_by_mdl.candidate_group_cd ||
               '/' || lst_sml_by_mdl.item_key ||
               '/' || replace(lst_sml_by_mdl.period_from, '-', '') || '_' || replace(lst_sml_by_mdl.period_to, '-', '') ||
               '/' || to_char(lst_sml_by_mdl.last_created_at, 'YYYYMMDD_HH24MISS_MS') ||
               '/' || lst_sml_by_mdl.simulation_key ||
               '/' || lst_sml_by_mdl.simulation_key || '_DATA.tsv' as s3_key
        from lst_icm
				/* item_key当たり最新のitem_current_modelデータで絞る */
				join lst_sml_by_mdl
                      on lst_sml_by_mdl.simulation_key = lst_icm.simulation_key
    """

    sql_select_item_crt_mdl_analysis = """
    	    with
    	    /* model_group_cdで絞るため  */
            mdl_grp as (
    			select model_group_cd, model_cd
    			from core_engine_test.m_model_group
    			where model_group_cd='{model_group_cd}'
    		),
    		/* 特定item_key, busidateの最新item_simulationデータ  */
            lst_sml as (
    			select *
    			from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key, model_cd) as max_time
    								FROM core_engine_test.item_simulation) as his
    			where created_at=max_time and item_key='{item_key}' and period_from = '{busidate}'
            ),
    		/* 特定item_keyの最新item_current_modelデータ：Modal画面で選ばれているデータ  */
    		lst_icm as (
    			select *
    			from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_time
    								FROM core_engine_test.item_current_model) as his
    			where created_at=max_time and item_key='{item_key}'
    		),
    		/* model_group_cdで絞ったmodel_cdでlst_icm結果を絞る  */
    		lst_icm_by_mdl as (
    			select lst_icm.*
    			from lst_icm
    			inner join mdl_grp
    				on mdl_grp.model_cd = lst_icm.model_cd
    		),
    		/* engine_cd, engine_version, candidate_group_cdをjoinするため  */
    		mdl as (
    			select *
    			from core_engine_test.m_model
    		)

            select '{s3_bucket_name}' as s3_bucket_name,
                   mdl.engine_cd ||
                   '/' || mdl.engine_version ||
                   '/' || mdl.candidate_group_cd ||
                   '/' || lst_sml.item_key ||
                   '/' || replace(lst_sml.period_from, '-', '') || '_' || replace(lst_sml.period_to, '-', '') ||
                   '/' || to_char(lst_sml.last_created_at, 'YYYYMMDD_HH24MISS_MS') ||
                   '/' || lst_sml.simulation_key ||
                   '/' || lst_sml.simulation_key || '_DATA.tsv' as s3_key
            from lst_icm_by_mdl
    				/* item_key当たり最新のitem_current_modelデータで絞る */
    				join lst_sml
                          on lst_icm_by_mdl.item_key = lst_sml.item_key
                                and lst_icm_by_mdl.model_cd = lst_sml.model_cd
    				left join mdl
    				      on mdl.model_cd = lst_icm_by_mdl.model_cd
        """

    sql_select_analysis = """
        with sml as (
            select *
            from core_engine_test.item_simulation
            where simulation_key = '{simulation_key}'
        )

        select '{s3_bucket_name}' as s3_bucket_name,
        mdl.engine_cd ||
        '/' || mdl.engine_version ||
        '/' || mdl.candidate_group_cd ||
        '/' || sml.item_key ||
        '/' || replace(sml.period_from, '-', '') || '_' || replace(sml.period_to, '-', '') ||
        '/' || to_char(sml.last_created_at, 'YYYYMMDD_HH24MISS_MS') ||
        '/' || simulation_key ||
        '/' || simulation_key || '_DATA.tsv' as s3_key,
        sml.period_from as busidate,
        item.closing_day
        from sml
            join core_engine_test.m_item as item
                on item.item_key = sml.item_key
            join core_engine_test.m_model as mdl
                on sml.model_cd = mdl.model_cd
    """

    sql_select_kpi = """
  with ptn as (
                select *
                from core_engine_test.item_model_map
            ),
            biz as (
                select item_key,
                       to_char(max(busidate), 'YYYY-MM-DD') as bizdate
                from core_engine_test.item_busidate
                group by item_key
            ),
            max_sml as (
                select item_key,
                       model_cd,
                       period_from,
                       max(last_created_at) as last_created_at
                from core_engine_test.item_simulation
                group by item_key, model_cd, period_from
            ),
            crt_mdl as (
                select his.item_key,
                       his.model_cd
                from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_time
                                    FROM core_engine_test.item_current_model) as his
                where created_at=max_time
            ),
            crt_smlt as (
                select cs.item_key,
                       cs.simulation_key
                from (SELECT *,MAX(created_at) OVER (PARTITION BY item_key) as max_time
                                    FROM core_engine_test.item_current_simulation) as cs
                where created_at=max_time
            ),
            sml as (
                select sml.*,
                       case when crt_mdl.item_key is null then 0 else 1 end as crt_mdl_flg,
                       case when crt_smlt.item_key is null then 0 else 1 end as crt_smlt_flg
                from core_engine_test.item_simulation sml
                         join ptn
                              on ptn.item_key = sml.item_key
                                  and ptn.model_cd = sml.model_cd
                         join biz
                              on biz.item_key = sml.item_key
                                  and biz.bizdate = sml.period_from
                         join max_sml
                              on max_sml.item_key = sml.item_key
                                  and max_sml.model_cd = sml.model_cd
                                  and max_sml.period_from = sml.period_from
                                  and max_sml.last_created_at = sml.last_created_at
                         left join crt_mdl
                                   on crt_mdl.item_key = sml.item_key
                                       and crt_mdl.model_cd = sml.model_cd
                         left join crt_smlt
                                   on crt_smlt.simulation_key = sml.simulation_key
                         join core_engine_test.m_item as item
                              on item.item_key = sml.item_key
            ),
            imk as (
                select imkm.*, mk.kpi_group_cd, mk.index
                from core_engine_test.item_model_kpi imkm
                left join core_engine_test.m_kpi mk
                      on imkm.kpi_cd = mk.kpi_cd
            ),
            hdr as (
                select sml.item_key,
                       itm.item_group_cd,
                       itm.stockout_flag,
                       sml.model_cd,
                       sml.simulation_key,
                       sml.crt_mdl_flg,
                       sml.crt_smlt_flg,
                       var.kpi_variation_cd,
                       imk.kpi_group_cd,
                       m_grp.index as kpi_group_index,
                       imk.kpi_cd,
                       imk.index as kpi_index
                from sml
                         join core_engine_test.m_item itm
                              on itm.item_key = sml.item_key
                         join imk
                              on imk.simulation_key = sml.simulation_key
                         join core_engine_test.m_kpi_group m_grp
                              on m_grp.kpi_group_cd = imk.kpi_group_cd
                         cross join core_engine_test.m_kpi_variation var
            ),
            kpi as (
                select sml.item_key,
                       sml.model_cd,
                       kpi.simulation_key,
                       m_kpi.kpi_group_cd,
                       m_kpi_group.index as kpi_group_index,
                       kpi.kpi_cd,
                       m_kpi.index as kpi_index,
                       kpi.kpi_variation_cd,
                       sml.crt_mdl_flg,
                       sml.crt_smlt_flg,
                       kpi.kpi_value,
                       kpi.prefix,
                       kpi.suffix,
                       kpi.kpi_alert,
                       kpi.default as default_flag,
                       itm.item_group_cd,
                       itm.stockout_flag
                from core_engine_test.item_model_kpi kpi
                         join core_engine_test.m_kpi m_kpi
                              on m_kpi.kpi_cd = kpi.kpi_cd
                         join core_engine_test.m_kpi_group m_kpi_group
                              on m_kpi_group.kpi_group_cd = m_kpi.kpi_group_cd
                         join core_engine_test.m_kpi_variation m_kpi_variation
                              on m_kpi_variation.kpi_variation_cd = kpi.kpi_variation_cd
                         join sml
                              on sml.simulation_key = kpi.simulation_key
                         join core_engine_test.m_item itm
                              on itm.item_key = sml.item_key
            ),
            st1 as (
                select item_key, sum(to_number(kpi.kpi_value, '000000000000')) as srt
                from kpi
                where kpi_group_cd = 'OFS'
                  and kpi_variation_cd = 'DAY'
                group by item_key
            ),
            st2 as (
                select item_group_cd, sum(to_number(kpi.kpi_value, '000000000000')) as srt
                from kpi
                where kpi_group_cd = 'OFS'
                  and kpi_variation_cd = 'DAY'
                group by item_group_cd
            ),
            dft as (
                select kpi.item_key,
                       kpi.model_cd,
                       kpi.simulation_key,
                       kpi.kpi_group_cd,
                       kpi.kpi_group_index,
                       kpi.kpi_cd,
                       kpi.kpi_index,
                       'DFT',
                       kpi.prefix,
                       kpi.kpi_value,
                       kpi.suffix,
                       kpi.kpi_alert,
                       kpi.crt_mdl_flg,
                       kpi.crt_smlt_flg,
                       kpi.item_group_cd,
                       kpi.stockout_flag
                from kpi
                where default_flag = 1
            ),
            var as (
                select hdr.item_key,
                       hdr.model_cd,
                       hdr.simulation_key,
                       hdr.kpi_group_cd,
                       hdr.kpi_group_index,
                       hdr.kpi_cd,
                       hdr.kpi_index,
                       hdr.kpi_variation_cd,
                       case
                           when kpi.kpi_variation_cd is not null
                               then kpi.prefix
                           else ''
                           end as kpi_prefix,
                       case
                           when kpi.kpi_variation_cd is not null
                               then kpi.kpi_value
                           else dft.kpi_value
                           end as kpi_value,
                       case
                           when kpi.kpi_variation_cd is not null
                               then kpi.suffix
                           else ''
                           end as kpi_suffix,
                       case
                           when kpi.kpi_variation_cd is not null
                               then kpi.kpi_alert
                           else dft.kpi_alert
                           end as kpi_alert,
                       hdr.crt_mdl_flg,
                       hdr.crt_smlt_flg,
                       hdr.item_group_cd,
                       hdr.stockout_flag
                from hdr
                         join dft
                                on dft.simulation_key = hdr.simulation_key
                                    and dft.kpi_cd = hdr.kpi_cd
                         left join kpi
                                on kpi.simulation_key = hdr.simulation_key
                                    and kpi.kpi_variation_cd = hdr.kpi_variation_cd
                                    and kpi.kpi_cd = hdr.kpi_cd
            ),
            ful as (
                select *
                from var
                union
                select *
                from dft
            ),
			mdl_grp as (
				select model_group_cd, model_cd
				from core_engine_test.m_model_group
			)

            select ful.*, mdl_grp.model_group_cd
            from ful
                     join st1 on st1.item_key = ful.item_key
                     join st2 on st2.item_group_cd = ful.item_group_cd
					 join mdl_grp on mdl_grp.model_cd = ful.model_cd
            order by kpi_variation_cd, st2.srt desc, ful.item_group_cd, stockout_flag, st1.srt desc, ful.item_key,
                     kpi_group_index, kpi_index
    """

    sql_select_busidate = """
        select bd.item_key, to_char(bd.busidate, 'YYYY-MM-DD') as busidate, item.item_group_cd
        from core_engine_test.item_busidate bd
        join core_engine_test.m_item item
            on bd.item_key = item.item_key
    """

    sql_select_candidate_detail = """
        select cgm.entity_candidate_cd, mec.entity_cd, mec.candidate_cd, cgm.candidate_group_cd
        from core_engine_test.candidate_group_map as cgm
        join core_engine_test.m_entity_candidate as mec
            on cgm.entity_candidate_cd = mec.entity_candidate_cd
    """

    sql_select_item_model_info = """
        select item_key, model_cd
        from core_engine_test.item_simulation
        where simulation_key='{simulation_key}'
    """

    sql_insert_item_model = """
        insert into core_engine_test.item_current_model (item_key, model_cd, created_by, created_at, updated_by, updated_at)
        values ('{item_key}', '{model_cd}', '{created_by}', current_timestamp, '{updated_by}', current_timestamp)
    """

    sql_insert_item_simulation = """
        insert into core_engine_test.item_current_simulation
        values {bulk_values}
    """

    sql_insert_entity = """
        WITH
            -- write the new values
            n(item_key, location_key, period_key, entity_cd, candidate_cd, stage_cd, adjustment_cd, value, value_type, created_by, created_at, updated_by, updated_at) AS (
                VALUES {bulk_values}
            )

        INSERT INTO core_engine_test.entity as o (item_key, location_key, period_key, entity_cd, candidate_cd, stage_cd, adjustment_cd, value, value_type, created_by, created_at, updated_by, updated_at)
        SELECT
            n.item_key,
            n.location_key,
            n.period_key,
            n.entity_cd,
            n.candidate_cd,
            n.stage_cd,
            n.adjustment_cd,
            n.value,
            n.value_type,
            n.created_by,
            n.created_at,
            n.updated_by,
            n.updated_at
        FROM n
        WHERE NOT EXISTS (
              select *
              from core_engine_test.entity as org
              where org.item_key = n.item_key and
                    org.location_key = n.location_key and
                    org.period_key = n.period_key and
                    org.entity_cd = n.entity_cd and
                    org.candidate_cd = n.candidate_cd and
                    org.value = n.value
        );
    """
