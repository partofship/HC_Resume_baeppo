import pathlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import about, contact, home, projects

app = FastAPI()
BASE_DIR = pathlib.Path(__file__).resolve().parent

# 정적 파일 제공
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# 라우터 등록
app.include_router(home.router)
app.include_router(projects.router)
app.include_router(about.router)
app.include_router(contact.router)
