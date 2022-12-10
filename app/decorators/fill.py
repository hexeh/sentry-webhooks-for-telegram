import logging

from dependency_injector.wiring import inject

from app.adapters import MapperStorage
from app.model.storage import ChatMapping
from app.util.ioc import get_dependency

logger = logging.getLogger(__name__)


def fill_chat(fn):
    @inject
    async def wrapper(
        event, storage: MapperStorage = get_dependency("storage"), **kwargs
    ):
        sender = kwargs.get("sender")
        if sender is None:
            sender = await event.get_sender()
            kwargs["sender"] = sender
        chat = kwargs.get("chat")
        if chat is None:
            chat = await event.get_chat()
            kwargs["chat"] = chat
        mapping = storage.get_entities_by_chat(ChatMapping, chat.id)
        return await fn(event, mapping=mapping, **kwargs)

    wrapper.__name__ = fn.__name__
    return wrapper
