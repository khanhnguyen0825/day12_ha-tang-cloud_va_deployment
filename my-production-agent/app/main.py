import time
import logging
import json
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Request, HTTPException
from contextlib import asynccontextmanager

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit, redis_client
from .cost_guard import check_budget, record_cost
from utils.mock_llm import ask

# Cấu hình Logging tập trung (JSON format)
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
is_ready = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    global is_ready
    logger.info("Starting Production AI Agent...")
    # Kiểm tra kết nối Redis
    try:
        if redis_client:
            redis_client.ping()
            logger.info("Connected to Redis successfully")
    except Exception as e:
        logger.warning(f"Could not connect to Redis: {e}")
    
    is_ready = True
    yield
    is_ready = False
    logger.info("Shutting down gracefully...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

@app.get("/health")
def health():
    """Liveness probe"""
    return {
        "status": "ok",
        "uptime": round(time.time() - START_TIME, 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/ready")
def ready():
    """Readiness probe"""
    if not is_ready:
        raise HTTPException(status_code=503, detail="Agent not ready")
    return {"status": "ready"}

@app.post("/ask")
async def ask_agent(
    request: Request,
    user_id: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit),
    _budget: None = Depends(check_budget)
):
    body = await request.json()
    question = body.get("question", "")
    
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    logger.info(json.dumps({
        "event": "request_received",
        "user": user_id,
        "question": question[:50] + "..."
    }))

    # Gọi Mock LLM
    response = ask(question)
    
    # Ghi nhận cost (giả lập token count)
    record_cost(user_id, len(question)//4, len(response)//4)

    logger.info(json.dumps({
        "event": "response_generated",
        "user": user_id
    }))

    return {
        "answer": response,
        "model": settings.LLM_MODEL,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
