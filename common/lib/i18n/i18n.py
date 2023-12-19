from common.lib.aipscm.data_access.i18n.AccessService import AccessService
import pandas as pd
import json


class I18n:
    def __init__(self, datas):
        self.datas = datas

    def __call__(self, func):
        def wrapper(**kwargs):
            lang = kwargs.get('lang', 'en')
            r = func(**kwargs)

            # rの結果とi18n_tの結果を紐づける
            df_row = pd.DataFrame(r)
            for data in self.datas:
                i18n_t = AccessService.translate(
                    table_name=data['table_name'], key_name=data['key_name'], lang=lang)
                df_i18n_t = pd.DataFrame(i18n_t)

                df_row = pd.merge(
                    df_row, df_i18n_t, how='left', on=[
                        data['key_name']])

            # DF to リスト
            fin: str = df_row.to_json(orient='index')
            fin: dict = json.loads(fin)

            result: list = []
            for key, value in fin.items():
                result.append(value)

            return result
        return wrapper
