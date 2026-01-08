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
    files = os.listdir(".")
    html_content = "<html><head><title>Index of /</title></head><body><h1>Index of /</h1><ul>"
    for file in files:
        html_content += f'<li><a href="/{file}">{file}</a></li>'
    html_content += "</ul></body></html>"
    return HTMLResponse(content=html_content)