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
            pic: str = d.get('pic')
            export_id: str = d.get('exportNo')
            buyer_name: str = d.get('buyerName')
            address: str = d.get('address')
            recipient: str = d.get('recipient')
            phone_num:str = d.get('phoneNum')
            requested_arrival_date: str = d.get('requestedArrivalDate')
            bill_type: str = d.get('billType')
            folder_id: str = d.get('folderId')
            delivery: str = d.get('delivery')
            delivery_type: str = d.get('deliveryType')
            remark: str = d.get('remark')

            # 메세지 생성
            slack_msg = SlackMsgCreator.get_slack_delivery_request_post_block(
                pic=pic,
                export_id=export_id,
                buyer_name=buyer_name,
                address=address,
                recipient=recipient,
                phone_num=phone_num,
                requested_arrival_date=requested_arrival_date,
                bill_type=bill_type,
                folder_id=folder_id,
                delivery=delivery,
                delivery_type=delivery_type,
                remark=remark
            )

            # 이미 생성된 export_id인지 확인
            slack_history_of_export_id = AccessService(GLOBAL).select_slack_history(export_id=export_id, delivery_type=delivery_type)

            # 이미 생성되어 있으면
            if len(slack_history_of_export_id) > 0:
                # 기존 slack id 취득
                slack_post_block_id = slack_history_of_export_id[0].get('slack_post_block_id')

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
                    msg_body=SlackMsgCreator.get_slack_updated_shipment_request(),
                    thread_ts=slack_post_block_id
                )

                # DB에 저장된 기존 slack 내용 수정
                AccessService(GLOBAL).update_slack_history(
                    export_id=export_id,
                    slack_post_block_id=slack_post_block_id,
                    pic=pic,
                    buyer_name=buyer_name,
                    address=address,
                    recipient=recipient,
                    recipient_phone_num=phone_num,
                    requested_arrival_date=requested_arrival_date,
                    bill_type=bill_type,
                    folder_id=folder_id,
                    delivery=delivery,
                    delivery_type=delivery_type,
                    remark=remark
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
                    export_id=export_id,
                    slack_post_block_id=slack_post_block_id,
                    pic=pic,
                    buyer_name=buyer_name,
                    address=address,
                    recipient=recipient,
                    recipient_phone_num=phone_num,
                    requested_arrival_date=requested_arrival_date,
                    bill_type=bill_type,
                    folder_id=folder_id,
                    delivery=delivery,
                    delivery_type=delivery_type,
                    remark=remark
                )

    except Exception as e:
        raise e