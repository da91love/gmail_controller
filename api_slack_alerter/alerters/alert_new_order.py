from datetime import datetime
from common.lib.ma.data_access.system.AccessService import AccessService
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *
from common.const.DB import *
def alert_new_order(data):
    try:
        slack = Slack()

        for d in data:
            slack_post_block_fr_api = {}
            
            slack_post_block_fr_api['pic'] = d.get('pic')
            slack_post_block_fr_api['export_id'] = d.get('exportNo')
            slack_post_block_fr_api['buyer_name'] = d.get('buyerName')
            slack_post_block_fr_api['address'] = d.get('address')
            slack_post_block_fr_api['recipient'] = d.get('recipient')
            slack_post_block_fr_api['recipient_phone_num'] = d.get('phoneNum')
            slack_post_block_fr_api['requested_arrival_date']= d.get('requestedArrivalDate')
            slack_post_block_fr_api['bill_type'] = d.get('billType')
            slack_post_block_fr_api['folder_id'] = d.get('folderId')
            slack_post_block_fr_api['delivery'] = d.get('delivery')
            slack_post_block_fr_api['delivery_type'] = d.get('deliveryType')
            slack_post_block_fr_api['remark'] = d.get('remark')

            # 메세지 생성
            slack_msg = SlackMsgCreator.get_slack_delivery_request_post_block(
                pic=slack_post_block_fr_api['pic'],
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

                        diff_col_as_text += f'"{key}: {bf} → {aft}" '

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

    except Exception as e:
        raise e