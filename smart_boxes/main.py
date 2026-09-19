import os
import sys

# 1. CHỈ ĐƯỜNG: Thêm thư mục hiện tại (smart_boxes) vào danh sách tìm kiếm của Python
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# 2. Bây giờ Python đã biết đường, nó sẽ tìm thấy file assembly.py
from assembly import LISHomeAssembly

app = FastAPI(title="LIS - SBBS Architecture", version="1.0")

# Mount static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR): 
    os.makedirs(STATIC_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Khởi tạo Assembly (Bộ điều phối)
home_assembly = LISHomeAssembly()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Assembly tự động lắp ráp và trả về giao diện hoàn chỉnh
    return home_assembly.render()

@app.get("/api/health")
def health_check():
    return {
        "system": "LIS",
        "architecture": "SBBS",
        "assembled_boxes": list(home_assembly.boxes.keys()),
        "status": "running"
    }