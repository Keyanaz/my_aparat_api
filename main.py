from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: str
    title: str
    icon: str
    type: str
    link: str

with open("data.json") as f:
    data = json.load(f)

items: List[Item] = [Item(**item) for item in data]

@app.get("/getNews")
def get_news():
    return items

# نمایش محتوای فایل‌ها به صورت متن ساده
@app.get("/main.py")
def show_main():
    with open("main.py") as f:
        content = f.read()
    return PlainTextResponse(content, media_type="text/plain")

@app.get("/data.json")
def show_data():
    with open("data.json") as f:
        content = f.read()
    return PlainTextResponse(content, media_type="application/json")

@app.get("/requirements.txt")
def show_req():
    with open("requirements.txt") as f:
        content = f.read()
    return PlainTextResponse(content, media_type="text/plain")

# صفحه ریشه با لینک به ۴ مورد و خوش‌آمدگویی
@app.get("/", response_class=HTMLResponse)
def root():
    html = """
    <html>
        <head>
            <title>Index of /pack/aparat</title>
            <style>
                body {font-family: Arial; margin: 40px; background: #f0f0f0;}
                h1 {color: #333;}
                p {font-size: 18px;}
                ul {list-style: none; padding: 0;}
                li {margin: 15px 0; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
                a {text-decoration: none; color: #007bff; font-size: 20px; font-weight: bold;}
                a:hover {text-decoration: underline;}
            </style>
        </head>
        <body>
            <h1>خوش آمدید به API شخصی</h1>
            <p>فایل‌های اصلی پروژه:</p>
            <ul>
                <li><a href="/getNews">getNews</a> → اطلاعات JSON (۴ آیتم)</li>
                <li><a href="/main.py">main.py</a> → کد منبع API</li>
                <li><a href="/data.json">data.json</a> → داده‌های خام</li>
                <li><a href="/requirements.txt">requirements.txt</a> → پکیج‌ها</li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(html)