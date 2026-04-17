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
4. **CMD vs ENTRYPOINT khac nhau the nao?** `CMD` cung cap lenh mặc định dễ dàng bị ghi đè, `ENTRYPOINT` quy định lệnh thực thi chính khó bị ghi đè hơn.

### Exercise 2.3: Image size comparison
- **Develop (python:3.11):** ~1.02 GB
- **Production (python:3.11-slim + Multi-stage):** ~165 MB
- **Difference:** ~84% reduction
- **Tai sao image nho hon?** Vi Stage 2 (runtime) chỉ lấy kết quả cuối cùng từ Stage 1 mà không bao gồm các công cụ build.

## Part 3: Cloud Deployment

### Exercise 3.1: Cloud deployment details
- **Public URL:** https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com
- **Platform:** Render (Dockerized)
- **Deployment Evidence:** [screenshots/render_live.png]

### Steps da thuc hien
1. Chuan bi source production tu thu muc `06-lab-complete/`.
2. Thay doi Dockerfile sang ban Multi-stage build on dinh (install prefix).
3. Deploy service len Render, Root Directory = `06-lab-complete`.
4. Thiet lap bien moi truong: `AGENT_API_KEY`, `PYTHONPATH`, `PORT`.
5. Verify public URL thay tra ve 200 OK cho endpoint `/health`.

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- **API Key Auth:**
```bash
curl -X POST https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ask \
	-H "Content-Type: application/json" \
	-d '{"question":"Hello"}'
```
Expected: `401 Unauthorized`

- **API Key Success:**
```bash
curl -X POST https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ask \
	-H "X-API-Key: 1234" \
	-H "Content-Type: application/json" \
	-d '{"question":"Hello"}'
```
Actual:
```json
{"question":"Hello","answer":"Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận.","model":"gpt-4o-mini","timestamp":"2026-04-17T..."}
```

- **Rate Limiting:**
```bash
for i in {1..15}; do
	curl -s -o /dev/null -w "%{http_code}\n" \
		-X POST https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com/ask \
		-H "X-API-Key: 1234" \
		-H "Content-Type: application/json" \
		-d '{"question":"test"}'
done
```
Actual output observed:
```text
200
200
200
200
200
200
200
200
200
200
429
429
429
429
429
```
Note: rate limiting now triggers correctly after Redis was connected.

### Exercise 4.4: Cost guard implementation
- **Cách tiếp cận:** Sử dụng `incrbyfloat` trong Redis để cộng dồn chi phí. 
- **Giới hạn:** $10/tháng (tương đương ~$0.33/ngày). Khi vượt quá trả về 402 Payment Required.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- **Health check:** Endpoint `/health` dùng để kiểm tra liveness của ứng dụng.
- **Readiness check:** Endpoint `/ready` dùng để kiểm tra các kết nối phụ thuộc.
- **Graceful shutdown:** Sử dụng `lifespan` và bắt tín hiệu `SIGTERM`.
- **Stateless design:** Toàn bộ state đã được chuyển từ memory sang Redis.
- **Final Result:** 20/20 Production Readiness checks passed!
