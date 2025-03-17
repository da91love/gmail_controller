import pydash as _
import requests
import uuid

from const.AUTH import *
from const.API import *
from const.PACKING_SPEC import *
from const.VISUAL_CONF import *

class Packing:
    def __init__(self, buyer_name):
        self.buyer_name = buyer_name
        self.boxes_info = {}
        self.box_packing_smr = {}
        self.pallet_packing = None
        self.pallet_packing_smr = None
        self.pallet_packing_detail_smr = None

    def calculate_box_packing(self, data):

        # 완포장 box 계산
        boxes_info = []
        left_prdts_info = []
        for order_info in data:
            # item code
            item_code = order_info['itemCode']
            order_vol = order_info["volume"]

            max_vol_of_box_d = MAX_PRDT_D_IN_BOX[item_code]
            max_vol_of_biggest_comm_box = (
                BOX_COMM_PRDT_NUM[item_code].get("BOX3", {}).get("MAX_VOLUME")
                or BOX_COMM_PRDT_NUM[item_code].get("BOX2", {}).get("MAX_VOLUME")
            )

            # Calculate number of full BOX_D and the leftover volume
            num_of_box_d = order_vol // max_vol_of_box_d
            left_num_of_prd = order_vol % max_vol_of_box_d

            num_of_prd_by_box = [max_vol_of_box_d for i in range(0, num_of_box_d)]
            if left_num_of_prd > 0: num_of_prd_by_box.append(left_num_of_prd)

            which_box = None
            for idx, prd_num in enumerate(num_of_prd_by_box):
                # 어떤 박스인지 찾아내기
                which_box = None
                if prd_num == max_vol_of_box_d:
                    which_box = 'BOX_D'
                else:
                    # Use the leftover volume to decide if an extra BOX_D is needed
                    if prd_num > max_vol_of_biggest_comm_box:
                        which_box = 'BOX_D'

                if which_box == 'BOX_D':
                    box_weight = BOX_D_SPEC[item_code]['WEIGHT']
                    box_scale = BOX_D_SPEC[item_code]['SCALE']
                    prdt_unit_weight = PRDT_SPEC[item_code]['WEIGHT']

                    box_info = {
                        'box_id': str(uuid.uuid4()),
                        'box_name': 'BOX_D',
                        'group': item_code,
                        'volume': prd_num,
                        'net_weight': prdt_unit_weight * prd_num,
                        'gross_weight': prdt_unit_weight * prd_num + box_weight,
                        'msmt': box_scale['WIDTH'] * box_scale['LENGTH'] * box_scale['HEIGHT'],
                        'width': box_scale['WIDTH'],
                        'length': box_scale['LENGTH'],
                        'height': box_scale['HEIGHT'],
                        'contents': {item_code: prd_num}
                    }

                    boxes_info.append(box_info)
                else:
                    left_prdts_info.append(
                        {
                            'item_code': item_code,
                            'volume': left_num_of_prd,
                        }
                    )

        # 남은 제품들을 합포장하는 알고리즘
        # bins 파라미터 생성
        bins = []
        for box in BOX_COMM_SPEC:
            bins.append({
                "id": box,
                "w": BOX_COMM_SPEC[box]['SCALE']['WIDTH'],
                "d": BOX_COMM_SPEC[box]['SCALE']['LENGTH'],
                "h": BOX_COMM_SPEC[box]['SCALE']['HEIGHT']
            })

        # items 파라미터 생성
        items = []
        for item in left_prdts_info:
            item_code = item['item_code']

            items.append({
                "id": item_code,
                "w": PRDT_SPEC[item_code]['SCALE']['WIDTH'],
                "d": PRDT_SPEC[item_code]['SCALE']['LENGTH'],
                "h": PRDT_SPEC[item_code]['SCALE']['HEIGHT'],
                "wg": PRDT_SPEC[item_code]['WEIGHT'],
                "q": item['volume'],
                "vr": 1
            })

        # request param 생성
        req = {
            "username": USER_NAME,
            "api_key": API_KEY,
            "bins": bins,
            "items": items,
            "params": VISUAL_CONF
        }

        # call api
        res = requests.post(BIN_PACKING_PACK_SHIPMENT_API_URL, json=req)

        if res.status_code == 200:
            json_res = res.json()
            bins_packed = json_res['response']['bins_packed']

            for bin_packed in bins_packed:
                box_name = bin_packed['bin_data']['id']
                box_weight = bin_packed['bin_data']['weight']
                box_scale = BOX_COMM_SPEC[box_name]['SCALE']
                items = bin_packed['items']

                contents = {}
                grouped_by_item_code = _.group_by(items, 'id')
                for item_code in grouped_by_item_code:
                    contents[item_code] = len(grouped_by_item_code[item_code])

                box_id = str(uuid.uuid4())
                boxes_info.append({
                    'box_id': box_id,
                    'box_name': box_name,
                    'group': box_id,
                    'volume': len(items),
                    'net_weight': box_weight,
                    'gross_weight': box_weight + BOX_COMM_SPEC[box_name]['WEIGHT'],
                    'msmt': box_scale['WIDTH'] * box_scale['LENGTH'] * box_scale['HEIGHT'],
                    'width': box_scale['WIDTH'],
                    'length': box_scale['LENGTH'],
                    'height': box_scale['HEIGHT'],
                    'contents': contents
                })

        elif res.status_code == 401:
            raise Exception

        # save as property
        self.boxes_info = boxes_info


    def set_box_packing_summary(self):

        # Calculate the smr
        packing_smr = []
        grouped_by_group = _.group_by(self.boxes_info, 'group')
        for group in grouped_by_group:
            group_info = grouped_by_group[group]

            if group_info[0]['box_name'] == "BOX_D":
                all_prd_volume = _.sum_by(group_info, 'volume')
                group = group_info[0]['group']
                box_name = 'BOX_D'
                box_quantity = len(group_info)
                net_weight = _.sum_by(group_info, 'net_weight')
                gross_weight = _.sum_by(group_info, 'gross_weight')
                msmt = _.sum_by(group_info, 'msmt')

                # Update order_info with the calculated values
                smr = {}
                smr["all_prd_volume"] = all_prd_volume
                smr["item_code"] = group
                smr["group"] = group
                smr["box_name"] = box_name
                smr["box_quantity"] = box_quantity
                smr["net_weight"] = net_weight
                smr["gross_weight"] = gross_weight
                smr["msmt"] = msmt

                packing_smr.append(smr)
            else:
                contents = group_info[0]['contents']

                for ic in contents:
                    all_prd_volume = contents[ic]
                    group = group_info[0]['group']
                    box_name = group_info[0]['box_name']
                    box_quantity = 1
                    net_weight = group_info[0]['net_weight']
                    gross_weight = group_info[0]['gross_weight']
                    msmt = group_info[0]['msmt']

                    # Update order_info with the calculated values
                    smr = {}
                    smr["all_prd_volume"] = all_prd_volume
                    smr["group"] = group
                    smr["item_code"] = ic
                    smr["box_name"] = box_name
                    smr["box_quantity"] = box_quantity
                    smr["net_weight"] = net_weight
                    smr["gross_weight"] = gross_weight
                    smr["msmt"] = msmt

                    packing_smr.append(smr)

        # save into property
        self.box_packing_smr = _.group_by(packing_smr, 'group')

    def calculate_pallet_packing(self, data):

        box_d = []
        leftBoxes = []
        # 팔레트의 최대 수량으로 나누어 나머지 박스들 리스트에 적재
        for box_info in data:
            item_code = box_info['group']

            # 합포장되어 단독박스에 들어있을 때는 left box로 격리
            try:
                max_box_d_in_pallet = None
                if self.buyer_name in EURO_PALLET_TG:
                    max_box_d_in_pallet = MAX_BOX_D_IN_PALLET['EURO'][item_code]
                else:
                    max_box_d_in_pallet = MAX_BOX_D_IN_PALLET['COMM'][item_code]
            except KeyError:
                del box_info['group']
                leftBoxes.append(box_info)
                continue

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

        all_calc_target_boxes = box_d + leftBoxes

        # 업체에 따라 상이한 팔레트 설정
        bins = None
        if self.buyer_name in EURO_PALLET_TG:
            bins = PALLET_SPEC['EURO']
        else:
            bins = PALLET_SPEC['COMM']


        bins_packed = []
        req = {
            "username": USER_NAME,
            "api_key": API_KEY,
            "bins": bins,
            "items": all_calc_target_boxes,
            "params": VISUAL_CONF
        }

        res = requests.post(BIN_PACKING_PACK_SHIPMENT_API_URL, json=req)

        if res.status_code == 200:
            json_res = res.json()

            for bin_packed in json_res['response']['bins_packed']:
                bins_packed.append(bin_packed)

        elif res.status_code == 401:
            raise Exception

        self.pallet_packing = bins_packed

        # # 업체에 따라 상이한 팔레트 설정
        # bins = None
        # if self.buyer_name in EURO_PALLET_TG:
        #     bins = PALLET_SPEC['EURO']
        # else:
        #     bins = PALLET_SPEC['COMM']
        #
        # bins_packed = []
        # req = {
        #     "username": USER_NAME,
        #     "api_key": API_KEY,
        #     "bins": bins,
        #     "items": data,
        #     "params": VISUAL_CONF
        # }
        #
        # res = requests.post(BIN_PACKING_PACK_SHIPMENT_API_URL, json=req)
        #
        # if res.status_code == 200:
        #     json_res = res.json()
        #     bins_packed = json_res['response']['bins_packed']
        #
        # elif res.status_code == 401:
        #     raise Exception
        #
        # self.pallet_packing = bins_packed

    def set_pallet_packing_smr(self):
        pallet_packing = self.pallet_packing

        packing_summary = []
        for idx, pp in enumerate(pallet_packing):
            bin_data = pp.get('bin_data')

            packing_summary.append({
                'width': bin_data['w'],
                'length': bin_data['d'],
                'height': bin_data['stack_height'],
                'net_weight': bin_data['weight'],
                'gross_weight': bin_data['gross_weight']
            })

        self.pallet_packing_smr = packing_summary

    def set_pallet_packing_details_smr(self):
        pallet_packing = self.pallet_packing

        pallet_packing_detail_smr = []
        box_id = 1
        for idx1, pl in enumerate(pallet_packing):
            items = pl.get('items')
            sorted_items = _.sort_by(items, 'id', True)

            for idx2, item in enumerate(sorted_items):
                # 완박스 인지 확인
                if item['id'] in PRODUCT_NAME.keys():
                    pallet_packing_detail_smr.append({
                        'pallet_id': idx1 + 1,
                        'box_id': box_id,
                        'product': PRODUCT_NAME[item['id']],
                        'box_name': 'BOX_D',
                        'q': int(_.round_((item['wg'] - (BOX_D_SPEC[item['id']])['WEIGHT']) / (PRDT_SPEC[item['id']])['WEIGHT'], 0)),
                    })

                    box_id += 1

                # 완박스가 아닌 혼합박스인 경우
                else:
                    # 혼합박스의 내용물 가져오기
                    box_info = _.find(self.boxes_info, {'box_id': item['id']})
                    contents = box_info['contents']
                    box_name = box_info['box_name']

                    for content in contents:
                        pallet_packing_detail_smr.append({
                            'pallet_id': idx1 + 1,
                            'box_id': box_id,
                            'product': PRODUCT_NAME[content],
                            'box_name': box_name,
                            'q': contents[content]
                        })

                    box_id += 1

        # box
        self.pallet_packing_detail_smr = pallet_packing_detail_smr