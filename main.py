from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  #for CORS wuthout localhost
from fastapi.responses import HTMLResponse  ##
from pydantic import BaseModel
from typing import List
import json
import os  ##

app = FastAPI()

# اضافه کردن CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # اجازه به همه (برای تست) بدون شبکه محلی
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

# لود داده از فایل JSON
with open('data.json') as f:
    data = json.load(f)

items: List[Item] = [Item(**item) for item in data]

@app.get("/getNews")
def get_news():
    return items

# برای تست محلی: uvicorn main:app --reload

#توضیح ساده:
#  این کد یک endpoint به نام /getNews می‌سازه که JSON array رو برمی‌گردونه.
#  FastAPI اتوماتیک JSON رو هندل می‌کنه و ساختار رو چک می‌کنه.



# endpoint جدید برای ریشه (/)
@app.get("/", response_class=HTMLResponse)    #یک صفحه HTML ساده برمی‌گرداند
def root():
    # لیست فایل‌ها و پوشه‌های فعلی (شامل images و videos اگر وجود داشته باشند)
    files = os.listdir(".")
    html_content = """
    <html>
        <head>
            <title>Index of /</title>
        </head>
        <body>
            <h1>Index of /</h1>
            <ul>
                <li><a href="/getNews">getNews</a></li>
    """
    for file in files:
        if file not in ['main.py', 'data.json', 'requirements.txt', '.gitignore']:  # فایل‌های غیرضروری را مخفی کنید
            html_content += f'<li><a href="/{file}">{file}</a></li>'
    html_content += """
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)