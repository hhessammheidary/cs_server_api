import logging
from fastapi import APIRouter
from ..models import ServerInstanceOut
from ..services.a2s_service import query_all
from ..config import load_servers

logger = logging.getLogger("app")
router = APIRouter()

@router.get("/serverList")
async def instance_all():
    """
    Returns:
      - instances: list of servers with server_name, ip, port, mod, players_current, players_max, online
      - total_players, server_count, queried_at (ISO)
    """
    logger.info("Received /instanceAll")
    summary = await query_all()
    return summary

@router.get("/serverIpList")
async def server_ip_list():
    logger.info("Received /serverIpList")
    return load_servers()
