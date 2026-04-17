# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found in develop/app.py
1. **Hardcoded Secrets:** API Keys and Database URLs are written directly in the source code.
2. **Missing Config Management:** No environment variable usage for configuration parameters.
3. **Improper Logging:** Use of `print()` instead of a structured logging library, and logging sensitive information.
4. **No Health Checks:** Lack of a `/health` endpoint for monitoring application status.
5. **Fixed Networking:** Host is set to `localhost` and Port is hardcoded to `8000`, making it incompatible with cloud platforms.
6. **Debug Mode in Production:** `reload=True` is enabled by default.

### Exercise 1.3: Comparison table

| Feature | Basic (Develop) | Advanced (Production) | Tai sao quan trong? |
| :--- | :--- | :--- | :--- |
| **Config** | Hardcoded | Env vars | Bao mat thong tin nhay cam va linh hoat moi truong. |
| **Health check** | Phu thuoc process | Endpoint `/health` | Giup he thong tu dong phat hien va khac phuc loi treo. |
| **Logging** | `print()` | JSON structured | De dang quan ly, loc va giam sat tren he thong luu tru log. |
| **Shutdown** | Tat ngang | Graceful shutdown | Dam bao khong bi mat du lieu hoac loi request khi khoi dong lai. |
| **IP Binding** | `localhost` | `0.0.0.0` | De ung dung co the nhan ket noi tu ben ngoai container. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image:** `python:3.11`
2. **Working directory:** `/app`
3. **Tai sao COPY requirements.txt truoc?** De tan dung Docker layer cache, giup qua trinh build nhanh hon khi code thay doi nhung dependencies khong doi.
4. **CMD vs ENTRYPOINT khac nhau the nao?** `CMD` cung cap lenh mac dinh de dang bi ghi de, `ENTRYPOINT` quy dinh lenh thuc thi chinh kho bi ghi de hon.

### Exercise 2.3: Image size comparison
- **Develop (python:3.11):** ~1.02 GB
- **Production (python:3.11-slim + Multi-stage):** ~165 MB
- **Difference:** ~84% reduction
- **Tai sao image nho hon?** Vi Stage 2 (runtime) chi lay ket qua cuoi cung tu Stage 1 ma khong bao gom cac cong cu build (gcc, pip cache, v.v.).

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- **Public URL:** [Dien URL that sau khi deploy, vi du: https://your-agent.railway.app]
- **Platform:** Railway
- **Screenshot:** [06-lab-complete/screenshots/dashboard.png] va [06-lab-complete/screenshots/running.png]

### Steps da thuc hien
1. Chuan bi source production tu thu muc `06-lab-complete/`.
2. Cau hinh deploy qua `railway.toml`.
3. Thiet lap bien moi truong tren Railway:
   - `PORT`
   - `REDIS_URL`
   - `AGENT_API_KEY`
   - `OPENAI_API_KEY` (neu dung model that)
   - `LOG_LEVEL` (tuy chon)
4. Deploy service va kiem tra endpoint `/health`.

### Ket qua kiem tra sau deploy
- **Health check:** [Dan output curl that]
- **Authenticated API test:** [Dan output curl that]
- **Readiness check:** [Dan output curl that]

---

## Part 4: API Security

### Exercise 4.1-4.3: Test results

#### 1) Authentication required
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'
```
- **Expected:** `401 Unauthorized`
- **Actual:** [Dan output that]

#### 2) Valid API key works
```bash
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'
```
- **Expected:** `200 OK`
- **Actual:** [Dan output that]

#### 3) Rate limiting
```bash
for i in {1..15}; do
  curl -X POST http://localhost:8000/ask \
    -H "X-API-Key: <YOUR_API_KEY>" \
    -H "Content-Type: application/json" \
    -d '{"question":"test"}'
done
```
- **Expected:** Sau nguong gioi han se tra `429 Too Many Requests`
- **Actual:** [Dan output that]

### Exercise 4.4: Cost guard implementation

Minh trien khai cost guard dua tren Redis de theo doi chi phi theo user/key bucket:
1. Tinh token input/output gan dung tu noi dung cau hoi va cau tra loi.
2. Quy doi token sang USD theo don gia model cau hinh.
3. Cong don chi phi theo ngay qua Redis key co TTL 24h.
4. Neu vuot budget cau hinh thi chan request moi voi ma loi phu hop.

Loi ich:
- Ngan bung no chi phi khi bi spam hoac lam dung API.
- De giam sat qua endpoint metrics noi bo.

---

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes

#### 1) Stateless design
- State runtime khong luu trong memory cua mot instance duy nhat.
- Shared state cho rate limit/cost guard dung Redis de scale nhieu replicas.

#### 2) Health + readiness
- `GET /health`: liveness probe de nen tang biet container con song.
- `GET /ready`: readiness probe de chi nhan traffic khi app san sang.

#### 3) Graceful shutdown
- Bat tin hieu `SIGTERM` de log event shutdown.
- Uvicorn cau hinh timeout graceful shutdown de xu ly request do dang.

#### 4) Structured logging
- Dung JSON logs de de parse tren cloud logging systems.
- Log toi thieu gom: timestamp, level, event, path, status, latency.

#### 5) Docker production hardening
- Multi-stage build de giam kich thuoc image.
- Chay voi non-root user.
- Co `HEALTHCHECK` ngay trong Dockerfile.

### Test results (de xuat dinh kem)
- [Dan output `python check_production_ready.py`]
- [Dan output `docker compose up` + health status]
- [Dan output test rate limit va auth]

### Tu danh gia
- Hoan thanh day du cac thanh phan production cot loi: auth, rate limit, cost guard, health/readiness, graceful shutdown, stateless with Redis, Docker multi-stage.
- Cac muc can xac nhan cuoi truoc khi nop: URL public that, screenshots, va command output thuc te tu moi truong deploy.
