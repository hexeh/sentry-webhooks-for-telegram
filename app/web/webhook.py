import logging
from datetime import datetime

from dependency_injector.wiring import inject
from fastapi import APIRouter, Request, Response, status
from jinja2 import Template

from app.adapters import MapperStorage, TelegramBot
from app.model.sentry import SentryWebhook
from app.model.storage import ChatMapping
from app.util.ioc import get_dependency

router = APIRouter(prefix="/webhook", tags=["webhook"])
log = logging.getLogger(__name__)


@router.post("/{project_id}")
@inject
async def process_webhook(
    project_id: int,
    request: Request,
    webhook: SentryWebhook,
    response: Response,
    bot: TelegramBot = get_dependency("bot"),
    storage: MapperStorage = get_dependency("storage"),
):
    try:
        mapping: ChatMapping = storage.get_entity_by_key(
            ChatMapping, project_id
        )
    except Exception:
        log.error(f"new webhook recieved for unconfigured slug - {project_id}")
        response.status_code = status.HTTP_403_FORBIDDEN
        return response
    scope = request.scope
    resource = scope.get("sentry-resource")
    log.info(f"new event with resource {resource} for slut {project_id}")
    if not scope.get("sentry-digest-valid", True):
        log.warning(f"{project_id} - {resource} - invalid digest")
        response.status_code = status.HTTP_403_FORBIDDEN
    else:
        # project_name, last_webhook
        mapping.last_webhook = datetime.utcnow()
        with storage.session.begin() as session:
            mapping = session.query(ChatMapping).get(project_id)
            mapping.last_webhook = datetime.utcnow()
            session.commit()
        try:
            message = Template(
                open(f"./app/messages/webhook/{resource}.html").read()
            )
        except FileNotFoundError:
            message = Template(
                open("./app/messages/webhook/not_implemented.html").read()
            )
        await bot.send_message(
            mapping.chat_id,
            message.render(
                resource=resource,
                project_name=mapping.project_name,
                event_id=webhook.data.event.event_id,
                level=webhook.data.event.level,
                logger=webhook.data.event.logger,
                message=webhook.data.event.message,
                issue_url=webhook.data.event.issue_url,
            ),
            "HTML",
        )
        response.status_code = status.HTTP_200_OK
