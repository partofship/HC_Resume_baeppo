import json
import os
import pathlib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# FastAPI 앱 생성
app = FastAPI()

# 경로 설정 - Vercel 환경 대응
if os.environ.get("VERCEL"):
    # Vercel 환경에서는 /var/task가 루트
    BASE_DIR = pathlib.Path("/var/task/app")
else:
    # 로컬 환경
    BASE_DIR = pathlib.Path(__file__).resolve().parent

# (삭제: 정적 파일 및) 템플릿 설정
# app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 로컬 개발 시에만 StaticFiles 마운트
if not os.environ.get("VERCEL"):
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# 프로젝트 데이터 로드
def load_projects():
    try:
        projects_file = BASE_DIR / "projects.json"
        with open(projects_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading projects: {e}")
        # 파일을 못 찾으면 빈 리스트 반환
        return []


# 메인 라우트 (원페이지)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    projects = load_projects()
    # 핵심 프로젝트만 필터링 (main=true 또는 상위 3개)
    featured_projects = [p for p in projects if p.get('main', False)][:3]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "projects": featured_projects,
            "contact_email": "strongandrew@naver.com"
        }
    )

# Health check endpoint (디버깅용)
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "vercel": os.environ.get("VERCEL", False),
        "base_dir": str(BASE_DIR),
        "templates_exists": (BASE_DIR / "templates").exists(),
        "projects_exists": (BASE_DIR / "projects.json").exists()
    }

# # 간단한 Contact API (미구현)
# @app.post("/api/contact")
# async def send_contact(
#         name: str = Form(...),
#         email: str = Form(...),
#         message: str = Form(...)
# ):
#     # 실제 이메일 전송 로직 구현(미구현), 이력서 pdf 다운로드 기능도?
#     print(f"Contact from {name} ({email}): {message}")
#     return {"status": "success", "message": "메시지가 전송되었습니다"}