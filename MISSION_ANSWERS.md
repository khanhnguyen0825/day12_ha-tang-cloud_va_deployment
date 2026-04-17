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

| Feature | Basic (Develop) | Advanced (Production) | Tại sao quan trọng? |
| :--- | :--- | :--- | :--- |
| **Config** | Hardcoded | Env vars | Bảo mật thông tin nhạy cảm và linh hoạt môi trường. |
| **Health check** | Phụ thuộc process | Endpoint `/health` | Giúp hệ thống tự động phát hiện và khắc phục lỗi treo. |
| **Logging** | `print()` | JSON structured | Dễ dàng quản lý, lọc và giám sát trên hệ thống lưu trữ log. |
| **Shutdown** | Tắt ngang | Graceful shutdown | Đảm bảo không bị mất dữ liệu hoặc lỗi request khi khởi động lại. |
| **IP Binding** | `localhost` | `0.0.0.0` | Để ứng dụng có thể nhận kết nối từ thế giới bên ngoài container. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image:** `python:3.11`
2. **Working directory:** `/app`
3. **Tại sao COPY requirements.txt trước?** Để tận dụng Docker layer cache, giúp quá trình build nhanh hơn khi code thay đổi nhưng dependencies không đổi.
4. **CMD vs ENTRYPOINT khác nhau thế nào?** `CMD` cung cấp lệnh mặc định dễ dàng bị ghi đè, `ENTRYPOINT` quy định lệnh thực thi chính khó bị ghi đè hơn.

### Exercise 2.3: Image size comparison
- **Develop (python:3.11):** ~1.02 GB
- **Production (python:3.11-slim + Multi-stage):** ~165 MB
- **Difference:** ~84% reduction
- **Tại sao image nhỏ hơn?** Vì Stage 2 (runtime) chỉ lấy kết quả cuối cùng từ Stage 1 mà không bao gồm các công cụ build (gcc, pip cache, v.v.).

## Part 3: Cloud Deployment
*(Đang chờ thực hiện trên GitHub Codespaces/Railway)*
