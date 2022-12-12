import logging
import re
from typing import Optional

from dependency_injector.wiring import inject
from jinja2 import Template
from telethon import events
from telethon.tl import types

from app.adapters import MapperStorage
from app.decorators import fill_chat
from app.model.storage import ChatMapping
from app.util.ioc import get_dependency

log = logging.getLogger(__name__)


@fill_chat
@inject
async def bind_chat(
    event: events.NewMessage,
    mapping: Optional[ChatMapping],
    chat: Optional[types.Chat],
    sender: Optional[types.User],
    storage: MapperStorage = get_dependency("storage"),
    owner_id: str = get_dependency("config.telegram.owner"),
):
    o = await event.client.get_entity(owner_id)
    chat_id = event.chat_id
    msg = event.message
    args = msg.message.split(" ")
    args = args[1:] if len(args) >= 1 else []
    if not sender or sender.id != owner_id:
        message = Template(
            open("./app/messages/commands/bind_restricted.html").read()
        )
        await event.reply(
            message.render(
                username=o.username,
                name=f'{o.first_name or ""} {o.last_name or ""}',
            ),
            parse_mode="HTML",
        )
        return
    if len(args) < 2:
        message = Template(
            open("./app/messages/commands/bind_noargs.html").read()
        )
        await event.reply(message.render(), parse_mode="HTML")
        return
    new_mapping = ChatMapping(
        project_id=args[0],
        project_name=args[1],
        chat_id=chat_id,
    )
    mapping = storage.get_entity_by_key(ChatMapping, args[0])
    if mapping is not None:
        message = Template(
            open("./app/messages/commands/bind_existing.html").read()
        )
        await event.reply(
            message.render(
                project_id=args[0],
                project_name=args[1],
                same_chat=mapping.chat_id == new_mapping.chat_id,
            ),
            parse_mode="HTML",
        )
        return
    storage.add_entity(new_mapping)
    mapping = storage.get_entities_by_chat(ChatMapping, chat_id)
    log.info(f"updated chat mapping: {mapping}")
    message = Template(
        open("./app/messages/commands/success_connect.html").read()
    )
    await event.reply(
        message.render(chat_id=chat_id, chats=mapping), parse_mode="HTML"
    )


def trigger_bind_chat():
    return [
        events.NewMessage(pattern=re.compile("^/bind_chat", flags=re.M | re.I))
    ]
