from operator import itemgetter
import pydash as _
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *

def alert_new_invoice(data):
    try:
        # Get data from API Gateway
        grouped_by_export_no = _.group_by(data, 'exportNo')

        # declare instance
        slack = Slack()
        for export_no in grouped_by_export_no:
            invoices = grouped_by_export_no[export_no]
            pi_request_date, export_no, buyer_name, country, currency = itemgetter('piRequestDate', 'exportNo', 'buyerName',
                                                                                   'country', 'currency')(invoices[0])

            summed_amount = _.sum_by(invoices, lambda x: int(float((x.get('amount')).replace(",", ""))))
            parsed_amount = f"{summed_amount:,} {currency}"

            slack_post_msg = SlackMsgCreator.get_slack_new_invoice_post_block(
                pi_request_date=pi_request_date,
                pi_no=('BSTSPI' + export_no[-11:]),
                export_no=export_no,
                buyer_name=buyer_name,
                country=country,
                summed_amount=parsed_amount
            )

            res = slack.add_post(
                channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                msg_type=MSG_TYPE['BLOCK'],
                msg_body=slack_post_msg
            )

            thread_ts = res.text

            for export_info in grouped_by_export_no[export_no]:
                productName, productCode, quantity = itemgetter('productName', 'productCode', 'quantity')(export_info)

                slack_reply_msg = SlackMsgCreator.get_slack_new_invoice_details_reply_block(
                    productName=productName,
                    productCode=productCode,
                    quantity=quantity
                )

                slack.add_reply(
                    channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                    msg_type=MSG_TYPE['BLOCK'],
                    msg_body=slack_reply_msg,
                    thread_ts=thread_ts
                )
    except Exception as e:
        raise e