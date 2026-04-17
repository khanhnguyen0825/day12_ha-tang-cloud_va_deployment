# Deployment Information

## Public URL
https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com

## Platform
Render

## Source Folder
`06-lab-complete/`

## Test Commands

### Health Check
```bash
curl https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/health
# Actual: {"status":"ok","version":"1.0.0","environment":"production",...}
```

### Readiness Check
```bash
curl https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ready
# Actual: {"ready": true}
```

### Authentication Required (Should Fail Without Key)
```bash
curl -X POST https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 401 Unauthorized
```

### API Test (With Authentication)
```bash
curl -X POST https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: 200 OK
```

### Rate Limit Test
```bash
for i in {1..15}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ask \
    -H "X-API-Key: YOUR_KEY" \
    -H "Content-Type: application/json" \
    -d '{"question":"load test"}'
done
# Actual during latest run: 200 for the first requests, then 429 for the remaining requests
```

## Environment Variables Set
- ENVIRONMENT=production
- DEBUG=false
- PORT (provided by Render)
- REDIS_URL=redis://red-d7h06i1kh4rs73afuqt0:6379
- AGENT_API_KEY
- JWT_SECRET
- OPENAI_API_KEY
- RATE_LIMIT_PER_MINUTE
- DAILY_BUDGET_USD
- APP_VERSION

## Screenshots
- [Deployment dashboard](06-lab-complete/screenshots/dashboard.png)
- [Service running](06-lab-complete/screenshots/running.png)
- [Test results](06-lab-complete/screenshots/test.png)

## Validation Notes
- Điền URL thật sau khi deploy thành công.
- Chạy lại toàn bộ test commands và dán output quan trọng vào phần nộp bài nếu giảng viên yêu cầu.
- Không commit giá trị secret thật vào repo.
