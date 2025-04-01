from operator import itemgetter
import pydash as _

from common.lib.ma.data_access.system.AccessService import AccessService
from common.const.DB import *
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *
from ..const.DOC_TYPE import *

def alert_new_invoice(data):
    try:
        # declare instance
        slack = Slack()
        for dt in data:
            invoices = data[dt]

            # get value from payload
            pi_request_date, export_no, buyer_name, country_code, currency, delivery_type, pic, requester = itemgetter('piDate', 'exportNo', 'buyerName',
                                                                                   'countryCode', 'currency', 'deliveryType', 'pic', 'requester')(invoices[0])
            # define doc type
            doc_type = PI

            summed_amount = _.sum_by(invoices, lambda x: int(x.get('amount')))
            parsed_amount = f"{summed_amount:,} {currency}"

            slack_post_msg = SlackMsgCreator.get_slack_new_invoice_post_block(
                pic=pic,
                pi_request_date=pi_request_date,
                export_no=export_no,
                delivery_type=delivery_type,
                buyer_name=buyer_name,
                country=country_code,
                summed_amount=parsed_amount,
                invoices=invoices
            )

            # get process history from db
            slack_block_ids = AccessService(GLOBAL).select_is_in_process_history(delivery_type=delivery_type, export_id=export_no)

            if len(slack_block_ids) > 0:
                slack_block_id = slack_block_ids[0].get('slack_post_block_id')

                slack.update_post(
                    msg_type=MSG_TYPE['BLOCK'],
                    channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                    msg_body=slack_post_msg,
                    thread_ts=slack_block_id
                )

                # insert into operation process
                AccessService(GLOBAL).insert_op_process(
                    export_id=export_no,
                    delivery_type=delivery_type,
                    doc_type=doc_type,
                    requester=requester,
                    slack_post_block_id=slack_block_id
                )

            else:
                res = slack.add_post(
                    channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=slack_post_msg
                )

                thread_ts = res.text

                # insert into operation process
                AccessService(GLOBAL).insert_op_process(
                    export_id=export_no,
                    delivery_type=delivery_type,
                    doc_type=doc_type,
                    requester=requester,
                    slack_post_block_id=thread_ts
                )
    except Exception as e:
        raise e