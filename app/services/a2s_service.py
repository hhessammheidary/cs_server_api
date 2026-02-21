import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

import a2s
from ..config import QUERY_TIMEOUT, load_servers

logger = logging.getLogger("app.services.a2s_service")

async def _a2s_info(addr: tuple) -> Any:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: a2s.info(addr, timeout=QUERY_TIMEOUT))

async def _a2s_players(addr: tuple) -> List[Dict[str, Any]]:
    loop = asyncio.get_running_loop()
    try:
        players = await loop.run_in_executor(None, lambda: a2s.players(addr, timeout=QUERY_TIMEOUT))
        return [{"name": p.name, "score": getattr(p, "score", None)} for p in players]
    except Exception as e:
        logger.debug("A2S players failed for %s:%s: %s", addr[0], addr[1], e)
        return []

async def query_instance(server: Dict[str, Any]) -> Dict[str, Any]:
    """
    Query one server (server dict must have ip, port, mod).
    Returns the fields required by the API.
    """
    ip = server.get("ip")
    port = int(server.get("port"))
    mod = server.get("mod", "")
    addr = (ip, port)
    result: Dict[str, Any] = {
        "server_name": None,
        "ip": ip,
        "port": port,
        "mod": mod,
        "players_current": None,
        "players_max": None,
        "online": False,
    }

    logger.debug("Querying A2S %s:%s", ip, port)
    try:
        info = await asyncio.wait_for(_a2s_info(addr), timeout=QUERY_TIMEOUT + 1.0)
        players = await asyncio.wait_for(_a2s_players(addr), timeout=QUERY_TIMEOUT + 1.0)

        result["server_name"] = info.server_name
        result["players_max"] = info.max_players
        result["players_current"] = len(players) if players else info.player_count
        result["online"] = True
    except asyncio.TimeoutError:
        result["online"] = False
        logger.warning("Timeout querying server %s:%s", ip, port)
    except Exception as exc:
        result["online"] = False
        logger.error("Error querying server %s:%s -> %s", ip, port, exc, exc_info=True)

    return result

async def query_all() -> Dict[str, Any]:
    servers = load_servers()
    tasks = [query_instance(s) for s in servers]
    results = await asyncio.gather(*tasks)
    total = sum(r["players_current"] or 0 for r in results if isinstance(r.get("players_current"), int))
    return {
        "instances": results,
        "total_players": total,
        "server_count": len(results),
        "queried_at": datetime.utcnow().isoformat() + "Z"
    }
