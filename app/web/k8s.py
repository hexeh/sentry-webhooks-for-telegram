from fastapi import APIRouter
from starlette import status

router = APIRouter(tags=["k8s"])


@router.get("/healthz", response_model=dict, status_code=status.HTTP_200_OK)
async def healthz():
    return {}


@router.get("/readiness", response_model=dict, status_code=status.HTTP_200_OK)
async def readiness():
    return {}
