from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os  # اضافه‌شده


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

with open('data.json') as f:
    data = json.load(f)

items: List[Item] = [Item(**item) for item in data]

@app.get("/getNews")
def get_news():
    return items

@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <html>
        <head><title>Index of /pack/aparat</title>...</head>
        <body>
            <h1>Index of /pack/aparat</h1>
            <ul>
                <li class="highlight"><a href="/getNews">getNews.php</a> → اطلاعات اصلی (JSON)</li>
                <li><a href="/main.py">main.py</a></li>
                <li><a href="/data.json">data.json</a></li>
                <li><a href="/requirements.txt">requirements.txt</a></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)