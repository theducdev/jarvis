from fastapi import APIRouter, Request
import psutil
import platform
from datetime import datetime
from src.api.v1.endpoints.websocket import manager as ws_manager

router = APIRouter()


@router.post("/wake")
async def wake_event(request: Request):
    """Triggered by clap-wake-listener on double-clap. Broadcasts 'wake' to all WS clients."""
    client_host = request.client.host if request.client else "unknown"
    if client_host not in ("127.0.0.1", "::1", "localhost"):
        return {"ok": False, "error": "wake events must originate from localhost"}
    await ws_manager.broadcast({
        "type": "wake",
        "data": {"timestamp": datetime.now().isoformat()}
    })
    return {"ok": True, "clients": len(ws_manager.active_connections)}


@router.get("/health")
async def system_health():
    """Get system health information"""
    try:
        # Use interval=0 to get instantaneous CPU reading (non-blocking)
        cpu_percent = psutil.cpu_percent(interval=0)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "memory_total": memory.total,
            "memory_used": memory.used,
            "disk_usage": disk.percent,
            "system": f"{platform.system()} {platform.release()}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        # Return graceful fallback if anything fails
        return {
            "status": "healthy",
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0,
            "system": "Unknown",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }