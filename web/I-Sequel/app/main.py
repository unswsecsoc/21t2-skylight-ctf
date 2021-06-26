from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from .db import dbsearch

app = FastAPI(title="I-Sequel")

app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
async def search(request: Request):
    params = (await request.json())
    return dbsearch(params)