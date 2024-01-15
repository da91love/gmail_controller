import requests
import json

from common.const.API_URL import *

class Slack:
    def __init__(self):
        pass


    def add_post(self,channel_id, msg_type, msg_body):
        try:
            slack_res = requests.post(SLACK_API['ADD_POST'], data={
                'type': msg_type,
                'channel': channel_id,
                'msg': msg_body,
            })

            return slack_res
        except Exception as e:
            raise e


    def add_reply(self,channel_id, msg_type, msg_body, thread_ts):
        try:
            slack_res = requests.post(SLACK_API['ADD_POST'], data={
                'type': msg_type,
                'channel': channel_id,
                'msg': msg_body,
                'thread_ts': thread_ts
            })

            return slack_res
        except Exception as e:
            raise e



    def update_post(self,channel_id, msg_type, msg_body, thread_ts):
        try:
            slack_res = requests.post(SLACK_API['UPDATE_POST'], data={
                'type': msg_type,
                'channel': channel_id,
                'msg': msg_body,
                'thread_ts': thread_ts
            })

            return slack_res
        except Exception as e:
            raise e