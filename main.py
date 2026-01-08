from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import json

app = FastAPI(
    title="Aparat API",
    description="API ساده برای دسترسی به اطلاعات فیلم‌ها",
    version="1.0.0"
)

# CORS برای امنیت – محدود به دامنه اپلیکیشن (جایگزین * با دامنه واقعی اپ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # برای تست؛ در تولید به ["https://your-app-domain.com"] تغییر دهید
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

# بارگذاری داده از data.json
with open("data.json") as f:
    data = json.load(f)

items: List[Item] = [Item(**item) for item in data]

# endpoint اصلی برای بازگشت JSON
@app.get("/getNews")
def get_news():
    return items

# صفحه ریشه – فقط لینک به /getNews و /docs (داکیومنت)
@app.get("/")
def root():
    return JSONResponse({
        "message": "API فعال است. برای دسترسی به اطلاعات، از /getNews استفاده کنید.",
        "documentation": "/docs (برای داکیومنت تعاملی Swagger)",
        "getNews": "/getNews (اطلاعات JSON)"
    })