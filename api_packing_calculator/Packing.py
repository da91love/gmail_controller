import pydash as _
import requests

from const.AUTH import *
from const.API import *
from const.PACKING_SPEC import *
from const.VISUAL_CONF import *

class Packing:
    def __init__(self):
        self.boxes_info = {}
        self.packing_smr = {}
        self.result = None

    def calculate_box_packing(self, order_info):
        # item code
        item_code = order_info['itemCode']

        # Get all box information (assumed to be provided by get_box_info())
        all_box_info = BOX_INFO
        item_info = all_box_info[order_info["itemCode"]]
        box_d_info = item_info["BOX_INFO"]["BOX_D"]
        comm_box_info = item_info["BOX_INFO"]["COMM_BOX"]

        max_vol_of_box_d = box_d_info["MAX_VOLUME"]
        order_vol = order_info["volume"]

        # Get the maximum volume from BOX3 if available, otherwise use BOX2
        max_vol_of_biggest_comm_box = (
                comm_box_info.get("BOX3", {}).get("MAX_VOLUME")
                or comm_box_info.get("BOX2", {}).get("MAX_VOLUME")
        )

        # Calculate number of full BOX_D and the leftover volume
        num_of_box_d = order_vol // max_vol_of_box_d
        left_num_of_prd = order_vol % max_vol_of_box_d

        num_of_prd_by_box = [max_vol_of_box_d for i in range(0, num_of_box_d)]
        if left_num_of_prd > 0: num_of_prd_by_box.append(left_num_of_prd)

        boxes_info = []
        for idx, prd_num in enumerate(num_of_prd_by_box):
            if idx == 48:
                pass

            print(f'{item_code}_{idx}')
            # 어떤 박스인지 찾아내기
            which_box = None
            if prd_num == max_vol_of_box_d:
                which_box = 'BOX_D'
            else:
                # Use the leftover volume to decide if an extra BOX_D is needed
                if prd_num > max_vol_of_biggest_comm_box:
                    which_box = 'BOX_D'
                else:
                    # Otherwise, iterate through the available comm boxes to find a match
                    for box, box_value in comm_box_info.items():
                        if (box_value["MIN_VOLUME"] <= left_num_of_prd and left_num_of_prd <= box_value["MAX_VOLUME"]):
                            which_box = box
                            break

            d = {'BOX_D': box_d_info} | comm_box_info
            box_weight = d.get(which_box)['WEIGHT']
            box_scale = d.get(which_box)['SCALE']

            box_info = {
                'box_id': idx,
                'box_name': which_box,
                'volume': prd_num,
                'net_weight': item_info['PRDT_UNIT_WEIGHT'] * prd_num,
                'gross_weight': item_info['PRDT_UNIT_WEIGHT'] * prd_num + box_weight,
                'msmt': box_scale['WIDTH'] * box_scale['LENGTH'] * box_scale['HEIGHT'],
                'width': box_scale['WIDTH'],
                'length': box_scale['LENGTH'],
                'height': box_scale['HEIGHT']
            }

            boxes_info.append(box_info)

        # Calculate the smr
        all_prd_volume = sum(num_of_prd_by_box)
        box_quantity = len(boxes_info)
        net_weight = _.sum_by(boxes_info, 'net_weight')
        gross_weight = _.sum_by(boxes_info, 'gross_weight')
        msmt = _.sum_by(boxes_info, 'msmt')


        # Update order_info with the calculated values
        smr = {}
        smr["all_prd_volume"] = all_prd_volume
        smr["box_quantity"] = box_quantity
        smr["net_weight"] = net_weight
        smr["gross_weight"] = gross_weight
        smr["msmt"] = msmt

        # save into property
        self.boxes_info[item_code] = boxes_info
        self.packing_smr[item_code] = smr

    def caculate_pallet_packing(self, data):

        box_d = []
        leftBoxes = []
        # 팔레트의 최대 수량으로 나누어 나머지 박스들 리스트에 적재
        for box_info in data:
            item_code = box_info['group']
            max_box_d_in_pallet = MAX_BOX_D_IN_PALLET[item_code]
            box_q = box_info['q']

            if (box_q / max_box_d_in_pallet) >= 1 and box_info['box_type'] == 'BOX_D':
                surplus_boxes = box_q % max_box_d_in_pallet

                if surplus_boxes == 0:
                    box_d.append(box_info)
                else:
                    box_info['q'] = box_q - surplus_boxes
                    copied_box_info = _.clone_deep(box_info)
                    copied_box_info['q'] = surplus_boxes
                    del copied_box_info['group']

                    box_d.append(box_info)
                    leftBoxes.append(copied_box_info)
            else:
                del box_info['group']
                leftBoxes.append(box_info)

        all_calc_target_boxes = [box_d, leftBoxes]

        bins_packed = []
        for tg_box in all_calc_target_boxes:
            req = {
                "username": USER_NAME,
                "api_key": API_KEY,
                "bins": PALLET_SPEC,
                "items": tg_box,
                "params": VISUAL_CONF
            }

            res = requests.post(BIN_PACKING_API_URL, json=req)

            if res.status_code == 200:
                json_res = res.json()

                for bin_packed in json_res['response']['bins_packed']:
                    bins_packed.append(bin_packed)

            elif res.status_code == 401:
                raise Exception

        self.result = bins_packed

        # bins_packed = []
        # req = {
        #     "username": USER_NAME,
        #     "api_key": API_KEY,
        #     "bins": PALLET_SPEC,
        #     "items": data,
        #     "params": VISUAL_CONF
        # }
        #
        # res = requests.post(BIN_PACKING_API_URL, json=req)
        #
        # if res.status_code == 200:
        #     json_res = res.json()
        #     bins_packed = json_res['response']['bins_packed']
        #
        # elif res.status_code == 401:
        #     raise Exception
        # self.result = bins_packed