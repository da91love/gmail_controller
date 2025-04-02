from operator import itemgetter
import pydash as _

from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *
from ..const.DOC_TYPE import *

def alert_new_pl(data):
    try:
        # declare instance
        slack = Slack()
        for dt in data:
            invoices = data[dt]

            # get value from payload
            export_no, requester, delivery_type = itemgetter('exportNo','requester','deliveryType')(invoices[0])
            # define doc type
            doc_type = PL

            # get process history from db
            slack_block_ids = AccessService(GLOBAL).select_is_in_process_history(delivery_type=delivery_type, export_id=export_no)

            try:
                slack_block_id = slack_block_ids[0].get('slack_post_block_id')
            except IndexError:
                raise Exception('PI가 생성되지 않았습니다.')

            # insert into operation process
            AccessService(GLOBAL).insert_op_process(
                export_id=export_no,
                doc_type=doc_type,
                delivery_type=delivery_type,
                requester=requester,
                slack_post_block_id=slack_block_id
            )

            # 업데이트 문구 리플라이
            slack.add_reply(
                channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                msg_type=MSG_TYPE['BLOCK'],
                msg_body=SlackMsgCreator.get_slack_new_doc_reply_block(requester=requester, doc_type=doc_type),
                thread_ts=slack_block_id
            )

    except Exception as e:
        raise e