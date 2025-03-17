from operator import itemgetter
import pydash as _
from common.slack.Slack import Slack
from common.slack.SlackMsgCreator import SlackMsgCreator
from common.const.SLACK import *

def alert_new_invoice(data):
    try:
        # declare instance
        slack = Slack()
        for dt in data:
            invoices = data[dt]
            pi_request_date, export_no, buyer_name, country_code, currency, delivery_type = itemgetter('piDate', 'exportNo', 'buyerName',
                                                                                   'countryCode', 'currency', 'deliveryType')(invoices[0])

            summed_amount = _.sum_by(invoices, lambda x: int(float((x.get('amount')).replace(",", ""))))
            parsed_amount = f"{summed_amount:,} {currency}"

            slack_post_msg = SlackMsgCreator.get_slack_new_invoice_post_block(
                pi_request_date=pi_request_date,
                export_no=export_no,
                buyer_name=buyer_name,
                country=country_code,
                summed_amount=parsed_amount
            )

            res = slack.add_post(
                channel_id=SLACK_GLOBAL_B2B_INVOICE_ID,
                msg_type=MSG_TYPE['BLOCK'],
                msg_body=slack_post_msg
            )

            thread_ts = res.text

            for invoice in data[dt]:
                product_name, product_code, quantity = itemgetter('productName', 'productCode', 'quantity')(invoice)

                slack_reply_msg = SlackMsgCreator.get_slack_new_invoice_details_reply_block(
                    productName=product_name,
                    productCode=product_code,
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