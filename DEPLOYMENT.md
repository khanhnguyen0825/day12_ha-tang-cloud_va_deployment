# Deployment Information

## Public URL
https://your-agent.railway.app

## Platform
Railway

## Source Folder
`06-lab-complete/`

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status":"ok", ...}
```

### Readiness Check
```bash
curl https://your-agent.railway.app/ready
# Expected: {"ready": true}
```

### Authentication Required (Should Fail Without Key)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 401 Unauthorized
```

### API Test (With Authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 200 OK
```

### Rate Limit Test
```bash
for i in {1..15}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST https://your-agent.railway.app/ask \
    -H "X-API-Key: YOUR_KEY" \
    -H "Content-Type: application/json" \
    -d '{"question":"load test"}'
done
# Expected: eventually 429
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- OPENAI_API_KEY
- RATE_LIMIT_PER_MINUTE
- DAILY_BUDGET_USD
- APP_VERSION
- ENVIRONMENT

## Screenshots
- [Deployment dashboard](06-lab-complete/screenshots/dashboard.png)
- [Service running](06-lab-complete/screenshots/running.png)
- [Test results](06-lab-complete/screenshots/test.png)

## Validation Notes
- Điền URL thật sau khi deploy thành công.
- Chạy lại toàn bộ test commands và dán output quan trọng vào phần nộp bài nếu giảng viên yêu cầu.
- Không commit giá trị secret thật vào repo.
