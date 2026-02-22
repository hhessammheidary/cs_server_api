from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .logging_config import setup_logging
from .api.server_routes import router as server_router
import logging, time

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title="CS1.6 A2S API")

# CORS: fully open (debug mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],     # optional: helps when you want to read custom headers in browser
    max_age=86400,            # cache preflight 24h
)

app.include_router(server_router)

# Optional: simple request logging (no auth)
@app.middleware("http")
async def log_middleware(request, call_next):
    start = time.time()
    logger.info("HTTP %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration = time.time() - start
    logger.info("Completed %s %s in %.3fs -> %s", request.method, request.url.path, duration, response.status_code)
    return response

@app.get("/")
async def root():
    return {"message": "Use /serverList to fetch servers info."}