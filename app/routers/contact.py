import json
import pathlib
import smtplib
from email.mime.text import MIMEText

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# ===== Contact Form (GET) =====
@router.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    with open(BASE_DIR.parent / "projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)

    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "projects": projects,
            "contact_email": settings.CONTACT_EMAIL,
        },
    )


# ===== Contact Form (POST - 메일 전송) =====
@router.post("/contact", response_class=HTMLResponse)
async def send_mail(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form("문의"),
    message: str = Form(...),
):
    try:
        # 메일 내용 작성
        body = f"보낸 사람: {name} ({email})\n\n{message}"
        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_USER
        msg["To"] = settings.EMAIL_USER

        # SMTP 연결 및 메일 전송
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.send_message(msg)

        result = "메일이 성공적으로 전송되었습니다."
    except Exception as e:
        result = f"메일 전송 실패 : {str(e)}"

    # 다시 contact.html 렌더링 (알림 메시지 표시)
    return templates.TemplateResponse(
        "contact.html", {"request": request, "projects": [], "result": result}
    )
