import time
import redis
from fastapi import HTTPException
from .config import settings

# Khởi tạo Redis client
# Lưu ý: Trong Docker Compose, host sẽ là 'redis' thay vì 'localhost'
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception:
    redis_client = None

def check_rate_limit(user_id: str):
    """
    Sử dụng Fixed Window algorithm với Redis.
    Giới hạn số request mỗi phút.
    """
    if not redis_client:
        # Fallback nếu không có Redis (cho môi trường dev không docker)
        return
        
    current_minute = int(time.time() / 60)
    key = f"rate_limit:{user_id}:{current_minute}"
    
    count = redis_client.get(key)
    if count and int(count) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_PER_MINUTE} requests per minute."
        )
    
    # Tăng count và set expire
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, 60)
    pipe.execute()
