import asyncio
import importlib
import logging
from typing import Any, Callable, Optional

from telethon import TelegramClient, connection
from telethon.sessions.memory import MemorySession
from telethon.tl.types import Message

log = logging.getLogger(__name__)


class TelegramBot:
    def __init__(
        self,
        token: str,
        session_name: str,
        api_id: Optional[int],
        api_hash: Optional[str],
        client: Optional[TelegramClient] = None,
        proxy: Optional[Any] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        self.session_name = session_name
        if client is None:
            if proxy:
                conn_type = connection.ConnectionTcpMTProxyAbridged
            else:
                conn_type = connection.tcpfull.ConnectionTcpFull
            client = TelegramClient(
                MemorySession(),
                api_id,
                api_hash,
                connection=conn_type,
                proxy=proxy,
                loop=loop,
                auto_reconnect=True,
            )
        self.client = client
        self.client_name = None
        self.instance = self.client.start(bot_token=token)

    def __call__(self) -> TelegramClient:
        return self.client

    def __assign_handler(self, handler: Callable, event: Any) -> None:
        log.info(f"added handler for event: {event}")
        self.client.add_event_handler(handler, event)

    async def connect(self) -> None:
        if self.instance is not None and asyncio.iscoroutine(self.instance):
            await self.instance
            bot = await self.client.get_me()
            self.client_name = f"@{bot.username}"
            log.info(f"init for {self.client_name}")
            self.prepare()

    async def disconnect(self) -> None:
        is_connected = self.client.is_connected()
        if is_connected:
            await self.client.disconnect()

    async def send_message(
        self, chat_id: Any, message: str, parse_mode: str
    ) -> Message:
        return await self.client.send_message(
            int(chat_id), message=message, parse_mode=parse_mode
        )

    def prepare(self, commands_path="app.commands"):
        try:
            command_handlers = importlib.import_module(commands_path)
        except ModuleNotFoundError:
            log.error("no commands to ad")
            return
        handlers_count = 0
        for command in dir(command_handlers):
            if command.startswith("handle_"):
                command_sign = command.replace("handle_", "")
                command_triggers = getattr(
                    command_handlers, f"trigger_{command_sign}"
                )()
                for cmd in command_triggers:
                    self.__assign_handler(
                        getattr(command_handlers, command), cmd
                    )
                handlers_count += 1
        log.info(f"added {handlers_count} handlers")
