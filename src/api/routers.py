from fastapi import APIRouter, Response
from ..utils.metrics import metrics
from ..utils.prometheus_metrics import export_metrics

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    return metrics.get_metrics()

@router.get("/prometheus")
async def get_prometheus_metrics():
    return Response(content=export_metrics(), media_type="text/plain")
