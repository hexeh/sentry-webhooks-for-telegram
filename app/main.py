import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI

from app.config import setup_config
from app.container import ApplicationContainer
from app.logger import setup_logger
from app.web import build_router, k8s
from app.web.middleware import SentryProcessMiddleware

setup_logger()


def create_container() -> ApplicationContainer:
    return setup_container()


def setup_container(
    container: Optional[ApplicationContainer] = None,
) -> ApplicationContainer:
    container = container or ApplicationContainer()
    setup_config(container.config)
    return container


def create_web_app(
    container: Optional[ApplicationContainer] = None,
) -> FastAPI:
    container = setup_container(container)
    app = container.app()
    app.state.container = container
    container.wire(packages=[sys.modules["app"]])
    main_router = build_router()
    app.include_router(main_router)
    app.include_router(k8s.router)
    app.add_middleware(
        SentryProcessMiddleware,
        sentry_secret=container.config.get("sentry.secret"),
    )
    app.add_event_handler("startup", container.init_resources)
    app.add_event_handler("shutdown", container.shutdown_resources)

    return app


def main() -> None:
    app = create_web_app()
    port = app.state.container.config.server.port()
    uvicorn.run(app, port=port, log_config=None)
