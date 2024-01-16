STATUS = {
    'OPEN': 'open',
    'CLOSE': 'close',
    'PENDING': 'pending',
    'TBD': 'tbd',
}

PROGRESS = {
    'NEGOTIATING': 'negotiating',
    'CONTRACT': 'contract',
    'DELIVERY': 'delivery',
    'PRE_APPROVAL': 'pre_approval',
    'PAYMENT': 'payment',
    'DEAL_FINISH': 'deal_finish',
}

EMS_DELIVERY_STATUS = {
    'On Its Way to Rincos Sorting Center': 'DeliverToFacility',
    'Shipment Picked up': 'PickupDone',
    'Handed over to korea post': 'HandToCarrierFacility',
    '접수': 'Registered',
    '발송': 'DeliverToFacility',
    '발송교환국에 도착': 'ArrivedAtFacility',
    '발송준비': 'ReadyForDelivery',
    '운송사 인계': 'HandToCarrierFacility',
    '항공사 인수': 'HandToFlight',
    '항공기 출발(예정,한국시간)': 'FlightDeparted',
    '상대국 도착': 'ArrivedAtAbroadCarrierFacility',
    '상대국 인계': 'HandToAbroadCarrierFacility',
    '교환국 도착': 'ArrivedAtCarrierFacility',
    '통관검사대기': 'ReadyForCustom',
    '통관 및 분류': 'CustomCheckDone',
    '도착': 'ArrivedAtCarrierFacility',
    '미배달': 'Undeliverable',
    '배달누락': 'DeliveryAttempted',
    '배달완료': 'Delivered',
}