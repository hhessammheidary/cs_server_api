from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from .logging_config import setup_logging
from .api.server_routes import router as server_router
from .config import API_KEY
import logging, time

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title="CS1.6 A2S API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(server_router)

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # Skip API key check for root endpoint + preflight requests
    if request.method == "OPTIONS" or request.url.path == "/":
        return await call_next(request)

    api_key = request.headers.get("X-API-Key") or request.query_params.get("X-API-Key")

    if not api_key or api_key != API_KEY:
        logger.warning("Unauthorized request to %s from %s", request.url.path, request.client.host)
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")

    start = time.time()
    logger.info("HTTP %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration = time.time() - start
    logger.info("Completed %s %s in %.3fs -> %s", request.method, request.url.path, duration, response.status_code)
    return response

@app.get("/")
async def root():
    return {"message": "Use /serverList to fetch servers info."}
