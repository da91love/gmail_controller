import os
import importlib

# singleton
config = None

def get_config():
    global config

    try:
        if config:
            return config
        else:
            env = os.environ.get('ENV', None)
            if env == "test":
                config_module = importlib.import_module('config.test')
            elif env == "demo":
                config_module = importlib.import_module('config.demo')
            elif env == "dev":
                config_module = importlib.import_module('config.development')
            elif env == "stg":
                config_module = importlib.import_module('config.staging')
            elif env == "prod":
                config_module = importlib.import_module('config.production')
            else:
                config_module = importlib.import_module('config.development')

            config = config_module.config
            return config

    except Exception as e:
        raise e