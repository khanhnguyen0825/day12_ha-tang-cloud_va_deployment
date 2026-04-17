import time
from fastapi import HTTPException
from .config import settings
from .rate_limiter import r

def check_budget(user_id: str):
    """
    Theo dõi chi phí sử dụng API của user lưu trong Redis.
    Giới hạn $10/tháng (được tính theo ngày trong lab này ~ $0.33/ngày).
    """
    if not r:
        return
        
    today = time.strftime("%Y-%m-%d")
    cost_key = f"cost:{user_id}:{today}"
    
    current_cost = float(r.get(cost_key) or 0.0)
    if current_cost >= settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=402,
            detail=f"Budget exceeded (${current_cost}). Limit is ${settings.MONTHLY_BUDGET_USD}/day."
        )

def record_cost(user_id: str, input_tokens: int, output_tokens: int):
    """
    Ghi nhận chi phí sau khi gọi LLM.
    Dùng giá GPT-4o-mini làm ví dụ.
    """
    if not r:
        return
        
    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
    today = time.strftime("%Y-%m-%d")
    cost_key = f"cost:{user_id}:{today}"
    
    pipe = r.pipeline()
    pipe.incrbyfloat(cost_key, cost)
    pipe.expire(cost_key, 24 * 3600)
    pipe.execute()
