from fastapi import APIRouter
from ..utils.metrics import metrics

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    return metrics.get_metrics()
