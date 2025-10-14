import json
import pathlib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
BASE_DIR = pathlib.Path(__file__).resolve().parent

# 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# 프로젝트 데이터 로드
def load_projects():
    with open(BASE_DIR / "projects.json", "r", encoding="utf-8") as f:
        return json.load(f)


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