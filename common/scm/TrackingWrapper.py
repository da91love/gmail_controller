import pydash as _
from mysql.connector.errors import *

from common.lib.ma.data_access.system.AccessService import AccessService
from common.scm.amazon.Amazon import Amazon
from common.scm.rincos.Rincos import Rincos
from common.util.logger_get import get_logger
from common.const.SCM import COURIER

logger = get_logger()
class TrackingWrapper:
    def __init__(self, tg_cp: str, invoices:list):
        self.tg_cp = tg_cp
        self.tg_invoices = list(filter(lambda k: k['courier']==self.tg_cp, invoices))
        self.instance = self.__get_instance()

    def update_tracking_history(self) -> list:
        uploaded_history = []
        for ivc in self.tg_invoices:
            order_id = ivc['order_id']
            invoice_id = ivc['invoice_id']

            tracking_history = self.instance.get_tracking_details(invoice_id=invoice_id)

            data = self.instance.convert_2_bsts_db(tracking_history)

            delivery_history = AccessService.select_delivery_history(invoice_id=invoice_id)

            if len(delivery_history) < len(data):
                # insert to data into delivery history tb
                for d in data:
                    try:
                        AccessService.insert_delivery_history(
                            order_id=order_id,
                            invoice_id=invoice_id,
                            delivery_status=d['delivery_status'],
                            event_time=d['event_time']
                        )

                        uploaded_history.append(d)
                    except IntegrityError as e:
                        continue

                # update data in delivery master
                AccessService.update_delivery_master(
                    order_id=order_id,
                    invoice_id=invoice_id,
                    delivery_status=data[-1]['delivery_status'],
                )

        return uploaded_history
    def __get_instance(self):
        try:
            if self.tg_cp == COURIER['RINCOS']:
                rincos = Rincos()
                return rincos
            elif self.tg_cp == COURIER['AMAZON']:
                amazon = Amazon()
                return amazon
        except Exception as e:
            raise e
