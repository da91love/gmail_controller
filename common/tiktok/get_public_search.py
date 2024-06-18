from tikapi import TikAPI, ValidationException, ResponseException
from common.util.get_config import get_config
from common.util.logger_get import get_logger

config = get_config()
logger = get_logger()
def get_public_search(tag: set):
    api_key = config['TIKAPI']['api_key']
    api = TikAPI(api_key)

    query = tag[0]
    error_tags = []

    try:
        response = api.public.search(
            category="videos",
            query=query,
            country='us'
        )

        loop = 1
        post_list_by_tag = []

        while (response):
            res = response.json()

            item_list = res.get('item_list')
            if item_list:
                for item in item_list:
                    post_list_by_tag.append(item)
            else:
                break

            logger.info(f'{query}:{loop} page finished')

            nextCursor = response.json().get('nextCursor')
            response = response.next_items()
            loop += 1

        logger.info(f'{query}: finished')

        return post_list_by_tag

    except ValidationException as e:
        logger.error(e, e.field)
        error_tags.append(query)
        pass

    except ResponseException as e:
        logger.error(e, e.response.status_code)
        error_tags.append(query)
        pass