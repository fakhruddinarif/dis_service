import midtransclient

from app.core.config import config

core_api = midtransclient.CoreApi(
    is_production = False if config.app_env == "local" else True,
    server_key = config.server_key_sandbox if config.app_env == "local" else config.server_key_production,
    client_key = config.client_key_sandbox if config.app_env == "local" else config.client_key_production
)

snap = midtransclient.Snap(
    is_production = False if config.app_env == "local" else True,
    server_key = config.server_key_sandbox if config.app_env == "local" else config.server_key_production,
    client_key = config.client_key_sandbox if config.app_env == "local" else config.client_key_production
)