import logging
import re
from typing import Optional

from dependency_injector.wiring import inject
from jinja2 import Template
from telethon import events

from app.decorators import fill_chat
from app.model.storage import ChatMapping

# from app.client import Storage


logger = logging.getLogger(__name__)


@fill_chat
@inject
async def check_chat(
    event: events.NewMessage,
    mapping: Optional[ChatMapping],
    # chat: Optional[types.Chat],
    # sender: Optional[types.User],
    # storage: Storage = get_dependency('storage')
):
    if mapping is None:
        await event.reply("No Sentry projects connected to this chat")
        return
    message = Template(open("messages/commands/chat_connections.html").read())
    await event.reply(message.render(chats=mapping), parse_mode="HTML")


def trigger_check_chat():
    return [
        events.NewMessage(
            pattern=re.compile("^/check_chat", flags=re.M | re.I)
        )
    ]
