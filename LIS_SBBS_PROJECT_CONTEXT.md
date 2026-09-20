# 📂 LIS SBBS PROJECT CONTEXT & STATE
**Ngày cập nhật:** 20/09/2026
**Phiên bản hiện tại:** v2.0 - Living Book with Structured Parser & Interactive Graph
**Dự án:** Learning Intelligence Infrastructure (LIS) - Trường ĐHSPKT Nam Định
**Kiến trúc:** Smart Black Box System (SBBS)

---

## 1. TRIẾT LÝ CỐT LÕI (Để AI luôn nhớ bối cảnh)
- **LIS (Learning Intelligence Infrastructure):** Không phải LMS quản lý điểm số, mà là hạ tầng tổ chức dòng chảy tri thức. Tri thức được phân rã thành "Nguyên tử" (Knowledge Atoms), kết nối thành "Vũ trụ" (Knowledge Graph), và tái sinh qua "Ngữ pháp" (Grammar Engine).
- **SBBS (Smart Black Box System):** Kiến trúc phần mềm Capability-First (Ưu tiên năng lực). 
  - **Smart Box:** Đóng gói năng lực độc lập, có Identity, Contract, và Knowledge Layer (để AI đọc hiểu).
  - **Smart Wire:** Lớp kết nối thông minh (Validate, Transform, Security).
  - **Assembly:** Khai báo kiến trúc hệ thống dưới dạng dữ liệu (Data-driven), không giấu trong code.

---

## 2. CẤU TRÚC THƯ MỤC HIỆN TẠI (`D:\LIS_NUTE\`)
```text
LIS_NUTE/
├── .gitignore
├── requirements.txt          (fastapi, uvicorn, PyPDF2, python-docx, python-multipart)
├── Dockerfile                (Đã tạo sẵn để deploy Render.com)
└── smart_boxes/
    ├── main.py               (Entry point, FastAPI app, đầy đủ API endpoints)
    ├── assembly.py           (Bộ điều phối lắp ráp các Box)
    ├── database.py           (SQLite CRUD cho Atoms, Relations, Sources)
    ├── atomic_parser.py      (Rule-based Structured Parser v2.0)
    ├── smart_wire.py         (ConfigWire đọc context.json)
    ├── context.json          (Dữ liệu động mẫu)
    ├── sample_data.txt       (Dữ liệu mẫu về Hạ tầng Niềm tin)
    ├── static/
    │   ├── logo.jpg
    │   └── background.png
    ├── SBBox_LIS_Hero/
    │   └── box.py            (Giao diện Hero 100vh, logo, background)
    ├── SBBox_Intelligence_Core/
    │   └── box.py            (3 cards: Human, AI, Knowledge Graph + Live Status Bar)
    ├── SBBox_AI_Chat_Widget/
    │   └── box.py            (Chat widget lơ lửng góc phải)
    ├── SBBox_Living_Book/
    │   └── box.py            (Minh họa SVG Knowledge Graph và danh sách Atom tĩnh)
    └── SBBox_Atom_Manager/
        └── box.py            (UI Quản lý: Upload file/text, Filter bar, Color-coded list, Vis.js Graph, Modal chi tiết)