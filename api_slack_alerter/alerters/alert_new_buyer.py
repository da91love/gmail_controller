from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *
def alert_new_buyer(data):
    try:
        corporate_name: str = data.get('corporate_name')
        business_name: int = data.get('business_name')
        buyer_type: int = data.get('buyer_type')
        is_exclusive: int = data.get('is_exclusive')
        country: str = data.get('country')
        pic: str = data.get('pic')
        url: str = data.get('url')
        mau: str = data.get('mau')

        slack = Slack()
        slack_msg = SlackMsgCreator.get_slack_new_buyer_post_block(
            corporate_name=corporate_name,
            business_name=business_name,
            buyer_type=buyer_type,
            is_exclusive=is_exclusive,
            country=country,
            url=url,
            mau=mau,
            pic=pic
        )

        slack.add_post(
            channel_id=SLACK_GLOBAL_EQB_CHANNEL_ID,
            msg_type=MSG_TYPE['BLOCK'],
            msg_body=slack_msg
        )
    except Exception as e:
        raise e