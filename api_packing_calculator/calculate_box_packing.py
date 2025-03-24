from const.PACKING_SPEC import *

def calculate_box_packing_spec(order_info):
    # Get all box information (assumed to be provided by get_box_info())
    all_box_info = BOX_INFO
    item_box_info = all_box_info[order_info["itemCode"]]
    comm_box = item_box_info["BOX_INFO"]["COMM_BOX"]

    max_vol_of_box_d = item_box_info["BOX_INFO"]["BOX_D"]["MAX_VOLUME"]
    order_vol = order_info["volume"]

    # Get the maximum volume from BOX3 if available, otherwise use BOX2
    max_vol_of_biggest_comm_box = (
        comm_box.get("BOX4", {}).get("MAX_VOLUME")
        or comm_box.get("BOX3", {}).get("MAX_VOLUME")
        or comm_box.get("BOX2", {}).get("MAX_VOLUME")
        or comm_box.get("BOX1", {}).get("MAX_VOLUME")
    )

    boxes = {}
    if order_vol >= max_vol_of_box_d:
        # Calculate number of full BOX_D and the leftover volume
        num_of_box_d = order_vol // max_vol_of_box_d
        left_num_of_prd = order_vol % max_vol_of_box_d

        boxes["BOX_D"] = num_of_box_d

        # Use the leftover volume to decide if an extra BOX_D is needed
        if left_num_of_prd > max_vol_of_biggest_comm_box:
            boxes["BOX_D"] += 1
        else:
            # Otherwise, iterate through the available comm boxes to find a match
            for box, comm_box_info in comm_box.items():
                if (comm_box_info["MIN_VOLUME"] <= left_num_of_prd and left_num_of_prd <= comm_box_info["MAX_VOLUME"]):
                    boxes[box] = 1
                    break

    else:
        # When the total order volume is less than the full BOX_D capacity,
        # treat the entire order volume as the leftover.
        left_num_of_prd = order_vol

        if order_vol > max_vol_of_biggest_comm_box:
            # If order volume is greater than the biggest comm box volume,
            # use one BOX_D.
            boxes["BOX_D"] = boxes.get("BOX_D", 0) + 1
        else:
            # Otherwise, find the appropriate comm box based on volume
            for box, comm_box_info in comm_box.items():
                if (comm_box_info["MIN_VOLUME"] <= order_vol  and order_vol <= comm_box_info["MAX_VOLUME"]):
                    boxes[box] = 1
                    break

    # Calculate the total number of boxes used
    box_quantity = sum(boxes.values())

    # Calculate net weight (unit weight multiplied by order volume)
    net_weight = item_box_info["PRDT_UNIT_WEIGHT"] * order_vol

    # Calculate the total weight of boxes used
    boxes_weight = 0
    for box, qty in boxes.items():
        if box in item_box_info["BOX_INFO"]:
            box_unit_weight = item_box_info["BOX_INFO"][box]["WEIGHT"]
        else:
            box_unit_weight = comm_box[box]["WEIGHT"]
        boxes_weight += qty * box_unit_weight

    gross_weight = net_weight + boxes_weight

    # Calculate the total measurement (msmt) for the boxes
    msmt = 0
    for box, qty in boxes.items():
        if box in item_box_info["BOX_INFO"]:
            scale = item_box_info["BOX_INFO"][box]["SCALE"]
        else:
            scale = comm_box[box]["SCALE"]
        box_unit_msmt = scale["WIDTH"] * scale["LENGTH"] * scale["HEIGHT"]
        msmt += qty * box_unit_msmt

    # Update order_info with the calculated values
    order_info["box_quantity"] = box_quantity
    order_info["net_weight"] = net_weight
    order_info["gross_weight"] = gross_weight
    order_info["msmt"] = msmt
    order_info["boxes"] = boxes

    print(boxes)
    print(order_info)
    return order_info
