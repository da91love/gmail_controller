# internal modules
import os
import logging
import pydash as _

# const
from src.const.LOCAL_PATH import *

# other modules
from common.util.FsUtil import FsUtil

# declare comm variable
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger('sLogger')

class TempSave:
    def __init__(self):
        self.cached_progress_rate = 0

    def save_file_in_mid(self, progress_rate: float, save_infos: list):
        try:
            if (progress_rate >= (self.cached_progress_rate + 0.02)) or (progress_rate == 1):

                # 데이타는 모두 기존데이터에 concat 방식으로 save됨
                for save_info in save_infos:
                    data, save_type, save_path = save_info['data'], save_info['save_type'], save_info['save_path']


                    if save_type == 'json':
                        # concat with existing data
                        db = FsUtil.open_json_2_json_file(save_path)
                        db += data

                        # save the file
                        FsUtil.save_json_2_json_file(db, save_path, 'utf-8')

                    elif save_type == 'csv':
                        # concat with existing data
                        db = FsUtil.open_csv_2_json_file(save_path)
                        db += data

                        # save the file
                        FsUtil.save_json_2_csv_file(db, save_path)

                # log
                logger.debug('mid save done: ' + str(_.round_(progress_rate*100, 2)) + '%')

                # update progress_rate
                self.cached_progress_rate = progress_rate

                return True

            else:
                return False
        except Exception as e:
            raise e