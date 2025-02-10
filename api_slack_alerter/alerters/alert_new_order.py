from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *
def alert_new_order(data):
    try:
        for d in data:
            pic: str = d.get('pic')
            buyer_name: int = d.get('buyerName')
            address: str = d.get('address')
            recipient: str = d.get('recipient')
            phone_num:str = d.get('phoneNum')
            requested_arrival_date: str = d.get('requestedArrivalDate')
            bill_type: str = d.get('billType')
            related_docs: str = d.get('relatedDocs')
            remark: str = d.get('remark')

            slack = Slack()
            slack_msg = SlackMsgCreator.get_slack_delivery_request_post_block(
                pic=pic,
                buyer_name=buyer_name,
                address=address,
                recipient=recipient,
                phone_num=phone_num,
                requested_arrival_date=requested_arrival_date,
                bill_type=bill_type,
                related_docs=related_docs,
                remark=remark
            )

            slack.add_post(
                channel_id=SLACK_GLOBAL_B2B_DELIVERY_REQUEST_ID,
                msg_type=MSG_TYPE['BLOCK'],
                msg_body=slack_msg
            )
    except Exception as e:
        raise e