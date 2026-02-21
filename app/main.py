from fastapi import FastAPI, Request
from .logging_config import setup_logging
from .api.server_routes import router as server_router
import logging, time

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title="CS1.6 A2S API")

app.include_router(server_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    logger.info("HTTP %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration = time.time() - start
    logger.info("Completed %s %s in %.3fs -> %s", request.method, request.url.path, duration, response.status_code)
    return response

@app.get("/")
async def root():
    return {"message": "Use /serverList to fetch servers info."}
