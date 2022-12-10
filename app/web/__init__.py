from fastapi import APIRouter

from . import webhook


def build_router():
    router = APIRouter(prefix="/v1")
    router.include_router(webhook.router)

    return router
