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
    # لیست تمام فایل‌ها و پوشه‌های فعلی (هیچ فایلی حذف نمی‌شود)
    files = os.listdir(".")
    html_content = """
    <html>
        <head>
            <title>Index of /</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
                h1 { color: #333; }
                ul { list-style-type: none; padding: 0; }
                li { margin: 10px 0; padding: 10px; background: white; border: 1px solid #ddd; border-radius: 5px; }
                a { text-decoration: none; color: #0066cc; font-size: 18px; font-weight: bold; }
                a:hover { text-decoration: underline; }
                .highlight { background: #e6f7ff; border: 2px solid #91d5ff; }
            </style>
        </head>
        <body>
            <h1>Index of /</h1>
            <ul>
                <li class="highlight"><a href="/getNews">getNews</a> (دریافت اطلاعات فیلم‌ها به صورت JSON)</li>
    """
    for file in sorted(files):
        if os.path.isdir(file):
            html_content += f'<li><a href="/{file}/">{file}/</a></li>'
        else:
            html_content += f'<li><a href="/{file}">{file}</a></li>'
    html_content += """
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)