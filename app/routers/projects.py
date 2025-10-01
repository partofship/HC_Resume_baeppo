import json
import pathlib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    with open(BASE_DIR.parent / "projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": projects}
    )
