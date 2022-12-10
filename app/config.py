import logging
import os

from dependency_injector import providers
from environs import Env

from app.util.config import ConfigEnvWrapper


def setup_config(config: providers.Configuration):
    from app.container import dynamic

    log = logging.getLogger(__name__)
    if log.isEnabledFor(logging.DEBUG):
        log.debug(f"environ: {os.environ}")
    env = Env()
    wrapper = ConfigEnvWrapper(config, env)
    wrapper.set_int(path="server.port", env="SERVER_PORT", default=9901)
    wrapper.set_str(path="security.token", env="SECURITY_TOKEN", default=None)
    wrapper.set_bool(
        path="security.token_enabled",
        env="SECURITY_TOKEN_ENABLED",
        default=False,
    )
    # Storage settings
    wrapper.set_str(
        path="storage.name",
        env="STORAGE_DB_NAME",
        default="sentry_telegram_service",
    )
    # Sentry settings
    wrapper.set_str(path="sentry.secret", env="SENTRY_SECRET")
    # Telegram bot settings
    wrapper.set_str(
        path="telegram.bot.session_name",
        env="TELEGRAM_BOT_SESSION_NAME",
        default="sentry_telegram_bot",
    )
    # find here: https://my.telegram.org/auth?to=apps
    wrapper.set_int(path="telegram.bot.api_id", env="TELEGRAM_BOT_API_ID")
    wrapper.set_str(path="telegram.bot.api_hash", env="TELEGRAM_BOT_API_HASH")
    wrapper.set_str(path="telegram.bot.token", env="TELEGRAM_BOT_TOKEN")
    wrapper.set_int(path="telegram.owner", env="TELEGRAM_OWNER")
    dynamic.config = config
