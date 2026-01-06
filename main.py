from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  #for CORS wuthout localhost
from pydantic import BaseModel
from typing import List
import json

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