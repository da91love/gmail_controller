from datetime import datetime
from common.lib.ma.data_access.system.AccessService import AccessService
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *
from common.const.DB import *
from ..const.DOC_TYPE import *

def alert_new_order(data):
    try:
        slack = Slack()

        # define doc type
        doc_type = OS

        for dt in data:
            tg = data[dt][0]
            
            slack_post_block_fr_api = {}

            slack_post_block_fr_api['brand'] = tg.get('brand')
            slack_post_block_fr_api['pic'] = tg.get('pic')
            slack_post_block_fr_api['requester'] = tg.get('requester')
            slack_post_block_fr_api['export_id'] = tg.get('exportNo')
            slack_post_block_fr_api['buyer_name'] = tg.get('buyerName')
            slack_post_block_fr_api['address'] = tg.get('address')
            slack_post_block_fr_api['recipient'] = tg.get('recipient')
            slack_post_block_fr_api['recipient_phone_num'] = tg.get('phoneNum')
            slack_post_block_fr_api['requested_arrival_date']= tg.get('requestedArrivalDate')
            slack_post_block_fr_api['bill_type'] = tg.get('billType')
            slack_post_block_fr_api['folder_id'] = tg.get('folderId')
            slack_post_block_fr_api['delivery'] = tg.get('delivery')
            slack_post_block_fr_api['delivery_type'] = tg.get('deliveryType')
            slack_post_block_fr_api['remark'] = tg.get('remark')

            # 메세지 생성
            slack_msg = SlackMsgCreator.get_slack_delivery_request_post_block(
                brand=slack_post_block_fr_api['brand'],
                pic=slack_post_block_fr_api['pic'],
                requester=slack_post_block_fr_api['requester'],
                export_id=slack_post_block_fr_api['export_id'],
                buyer_name=slack_post_block_fr_api['buyer_name'],
                address=slack_post_block_fr_api['address'],
                recipient=slack_post_block_fr_api['recipient'],
                recipient_phone_num=slack_post_block_fr_api['recipient_phone_num'],
                requested_arrival_date=slack_post_block_fr_api['requested_arrival_date'],
                bill_type=slack_post_block_fr_api['bill_type'],
                folder_id=slack_post_block_fr_api['folder_id'],
                delivery=slack_post_block_fr_api['delivery'],
                delivery_type=slack_post_block_fr_api['delivery_type'],
                remark=slack_post_block_fr_api['remark']
            )

            # 이미 생성된 export_id인지 확인
            slack_history_of_export_id = AccessService(GLOBAL).select_slack_history(export_id=slack_post_block_fr_api['export_id'], delivery_type=slack_post_block_fr_api['delivery_type'])

            # 이미 생성되어 있으면
            if len(slack_history_of_export_id) > 0:
                slack_post_block_fr_db = slack_history_of_export_id[0]

                # 기존 slack id 취득
                slack_post_block_id = slack_post_block_fr_db.get('slack_post_block_id')
                
                # api 정보와 db 정보 대조
                diff_col_as_text = ''
                for key in slack_post_block_fr_api:
                    if slack_post_block_fr_api[key] != slack_post_block_fr_db[key]:
                        bf = slack_post_block_fr_db[key]
                        aft = slack_post_block_fr_api[key]

                        diff_col_as_text += f'"{key}: {bf} → {aft}"\n'

                # 기존 slack update
                slack.update_post(
                    channel_id=SLACK_GLOBAL_B2B_DELIVERY_REQUEST_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=slack_msg,
                    thread_ts=slack_post_block_id
                )

                # 업데이트 문구 리플라이
                slack.add_reply(
                    channel_id=SLACK_GLOBAL_B2B_DELIVERY_REQUEST_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=SlackMsgCreator.get_slack_updated_shipment_request(diff_col_as_text),
                    thread_ts=slack_post_block_id
                )

                # DB에 저장된 기존 slack 내용 수정
                AccessService(GLOBAL).update_slack_history(
                    export_id=slack_post_block_fr_api['export_id'],
                    slack_post_block_id=slack_post_block_id,
                    pic=slack_post_block_fr_api['pic'],
                    requester=slack_post_block_fr_api['requester'],
                    brand=slack_post_block_fr_api['brand'],
                    buyer_name=slack_post_block_fr_api['buyer_name'],
                    address=slack_post_block_fr_api['address'],
                    recipient=slack_post_block_fr_api['recipient'],
                    recipient_phone_num=slack_post_block_fr_api['recipient_phone_num'],
                    requested_arrival_date=slack_post_block_fr_api['requested_arrival_date'],
                    bill_type=slack_post_block_fr_api['bill_type'],
                    folder_id=slack_post_block_fr_api['folder_id'],
                    delivery=slack_post_block_fr_api['delivery'],
                    delivery_type=slack_post_block_fr_api['delivery_type'],
                    remark=slack_post_block_fr_api['remark']
                )

                # insert into operation process
                AccessService(GLOBAL).insert_op_process(
                    export_id=slack_post_block_fr_api['export_id'],
                    delivery_type=slack_post_block_fr_api['delivery_type'],
                    doc_type=doc_type,
                    requester=slack_post_block_fr_api['requester'],
                    slack_post_block_id=slack_post_block_id
                )

                # get process history from db
                slack_block_ids = AccessService(GLOBAL).select_is_in_process_history(delivery_type=slack_post_block_fr_api['delivery_type'],
                                                                                     export_id=slack_post_block_fr_api['export_id'])
                slack_block_id = slack_block_ids[0].get('slack_post_block_id')

                # insert into operation process
                AccessService(GLOBAL).insert_op_process(
                    export_id=slack_post_block_fr_api['export_id'],
                    doc_type=doc_type,
                    delivery_type=slack_post_block_fr_api['delivery_type'],
                    requester=slack_post_block_fr_api['requester'],
                    slack_post_block_id=slack_block_id
                )

                # 업데이트 문구 리플라이
                slack.add_reply(
                    channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=SlackMsgCreator.get_slack_new_doc_reply_block(requester=slack_post_block_fr_api['requester'], doc_type=doc_type),
                    thread_ts=slack_block_id
                )

            else:
                # 신규 Slack post 작성
                res = slack.add_post(
                    channel_id=SLACK_GLOBAL_B2B_DELIVERY_REQUEST_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=slack_msg
                )

                slack_post_block_id = res.text

                # DB 등록
                AccessService(GLOBAL).insert_slack_history(
                    export_id=slack_post_block_fr_api['export_id'],
                    slack_post_block_id=slack_post_block_id,
                    pic=slack_post_block_fr_api['pic'],
                    requester=slack_post_block_fr_api['requester'],
                    brand=slack_post_block_fr_api['brand'],
                    buyer_name=slack_post_block_fr_api['buyer_name'],
                    address=slack_post_block_fr_api['address'],
                    recipient=slack_post_block_fr_api['recipient'],
                    recipient_phone_num=slack_post_block_fr_api['recipient_phone_num'],
                    requested_arrival_date=slack_post_block_fr_api['requested_arrival_date'],
                    bill_type=slack_post_block_fr_api['bill_type'],
                    folder_id=slack_post_block_fr_api['folder_id'],
                    delivery=slack_post_block_fr_api['delivery'],
                    delivery_type=slack_post_block_fr_api['delivery_type'],
                    remark=slack_post_block_fr_api['remark']
                )

                # get process history from db
                slack_block_ids = AccessService(GLOBAL).select_is_in_process_history(delivery_type=slack_post_block_fr_api['delivery_type'],
                                                                                     export_id=slack_post_block_fr_api['export_id'])
                slack_block_id = slack_block_ids[0].get('slack_post_block_id')

                # insert into operation process
                AccessService(GLOBAL).insert_op_process(
                    export_id=slack_post_block_fr_api['export_id'],
                    doc_type=doc_type,
                    delivery_type=slack_post_block_fr_api['delivery_type'],
                    requester=slack_post_block_fr_api['requester'],
                    slack_post_block_id=slack_block_id
                )

                # 업데이트 문구 리플라이
                slack.add_reply(
                    channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=SlackMsgCreator.get_slack_new_doc_reply_block(requester=slack_post_block_fr_api['requester'], doc_type=doc_type),
                    thread_ts=slack_block_id
                )

    except Exception as e:
        raise e