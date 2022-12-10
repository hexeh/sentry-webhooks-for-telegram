from dependency_injector import containers, providers
from dependency_injector.providers import Provider
from fastapi import FastAPI

from app.adapters import STORAGE, MapperStorage, TelegramBot
from app.model.storage import ChatMapping
from app.util.ioc import already_initialized


async def initialize_resources(bot: TelegramBot, storage: MapperStorage):
    storage.create_all()
    test_entity = storage.get_entity_by_key(ChatMapping, 123)
    if test_entity is not None:
        print(test_entity)
    await bot.connect()


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    app: Provider[FastAPI] = providers.Singleton(
        FastAPI, title="Sentry Webhook 2 Telegram"
    )
    storage: MapperStorage = providers.Singleton(already_initialized(STORAGE))
    bot: Provider[TelegramBot] = providers.Singleton(
        TelegramBot,
        session_name=config.telegram.bot.session_name,
        api_id=config.telegram.bot.api_id,
        api_hash=config.telegram.bot.api_hash,
        token=config.telegram.bot.token,
    )
    initializer = providers.Resource(
        initialize_resources, bot=bot, storage=storage
    )


dynamic = containers.DynamicContainer()
