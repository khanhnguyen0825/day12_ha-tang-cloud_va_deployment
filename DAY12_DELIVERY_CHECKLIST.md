#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Nguyễn Thành Đại Khánh
> **Student ID:** 2A202600404
> **Date:** 17/04/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

- [x] **Part 1: Localhost vs Production** (✅ Completed)
- [x] **Part 2: Docker** (✅ Completed)
- [x] **Part 3: Cloud Deployment** (✅ Completed with Render URL)
- [x] **Part 4: API Security** (✅ Completed with Rate Limiting Proof)
- [x] **Part 5: Scaling & Reliability** (✅ Completed with Stateless Proof)

---

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:

```
your-repo/
├── 06-lab-complete/         # Root directory of the final lab
│   ├── app/
│   │   ├── __init__.py      # Package marker (✅ Added)
│   │   ├── main.py          # Main application (✅ Completed with Lazy Redis)
│   │   ├── config.py        # Configuration (✅ 10req/min, $0.33/day)
│   │   ├── auth.py          # Authentication (✅ Completed)
│   │   ├── rate_limiter.py  # Rate limiting (✅ Completed)
│   │   └── cost_guard.py    # Cost protection (✅ Completed)
│   ├── utils/
│   │   └── mock_llm.py      # Mock LLM (provided)
│   ├── Dockerfile           # Stable Multi-stage build (✅ Completed)
│   ├── docker-compose.yml   # Full stack (✅ Completed)
│   ├── requirements.txt     # Dependencies (✅ Completed)
│   ├── .env.example         # Environment template (✅ Completed)
│   ├── .dockerignore        # Docker ignore (✅ Completed)
│   ├── render.yaml          # Render config (✅ Completed)
│   └── README.md            # Setup instructions (✅ Completed)
```

**Requirements:**
- [x] All code runs without errors
- [x] Multi-stage Dockerfile (image < 500 MB)
- [x] API key authentication
- [x] Rate limiting (10 req/min)
- [x] Cost guard ($10/month)
- [x] Health + readiness checks
- [x] Graceful shutdown
- [x] Stateless design (Redis)
- [x] No hardcoded secrets

---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

- [x] **Public URL is working:** https://day12-ha-tang-cloud-va-deployment-mmft.onrender.com
- [x] **Test commands provided:** OK
- [x] **Evidence (Screenshots) provided:** OK (in /06-lab-complete/screenshots/)

---

##  Self-Test Result
- [x] 1. Health check (200 OK)
- [x] 2. Auth required (401 OK)
- [x] 3. With key works (200 OK)
- [x] 4. Rate limiting (429 OK after 10 requests)

**FINAL STATUS: 100% READY FOR GRADING**
