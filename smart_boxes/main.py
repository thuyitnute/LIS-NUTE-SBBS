import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import sys

# Đảm bảo Python tìm thấy các module trong thư mục smart_boxes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SBBox_LIS_Hero.box import LISHeroBox

app = FastAPI(
    title="LIS - Learning Intelligence Infrastructure",
    description="Hạ tầng trí tuệ cho Đại học AI-Native",
    version="1.0"
)

# --- PHẦN SỬA LỖI STATIC ---
# Lấy đường dẫn tuyệt đối đến thư mục chứa file main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Tự động tạo thư mục static nếu chưa có (để không bị lỗi nữa)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Mount thư mục static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# ----------------------------

# Khởi tạo Smart Box
hero_box = LISHeroBox()

@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Trang chủ sử dụng SBBox-LIS-Hero
    """
    hero_html = hero_box.render({
        "slogan": "KIẾN TẠO - CHUẨN MỰC",
        "subtitle": "Learning Intelligence Infrastructure",
        "description": "Hạ tầng trí tuệ cho Đại học AI-Native",
        "cta_text": "KHÁM PHÁ LIS",
        "cta_link": "/about"
    })
    
    return hero_html

@app.get("/api/health")
def health_check():
    """
    API health check
    """
    return {
        "system": "LIS",
        "slogan": "KIẾN TẠO - CHUẨN MỰC",
        "status": "running",
        "smart_boxes": ["SBBox-LIS-Hero-001"]
    }