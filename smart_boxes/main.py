"""
LIS SBBS - Main Application Entry Point
Learning Intelligence Infrastructure - Smart Black Box System
Trường ĐHSPKT Nam Định
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import os
import uuid
import json

# Import từ các module trong smart_boxes
from .database import get_db, KnowledgeDatabase
from .ai_analyzer import get_analyzer
from .atomic_parser import AtomicParser

# Import các Smart Boxes
from .SBBox_LIS_Hero.box import HeroBox
from .SBBox_Intelligence_Core.box import IntelligenceCoreBox
from .SBBox_AI_Chat_Widget.box import AIChatWidgetBox
from .SBBox_Living_Book.box import LivingBookBox
from .SBBox_Atom_Manager.box import AtomManagerBox

# ============ KHỞI TẠO FASTAPI APP ============

app = FastAPI(
    title="LIS SBBS - Learning Intelligence Infrastructure",
    description="Smart Black Box System - Trường ĐHSPKT Nam Định",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Khởi tạo các Smart Boxes
hero_box = HeroBox()
intelligence_box = IntelligenceCoreBox()
chat_widget_box = AIChatWidgetBox()
living_book_box = LivingBookBox()
atom_manager_box = AtomManagerBox()

# Khởi tạo Parser
parser = AtomicParser()


# ============ PYDANTIC MODELS ============

class AtomCreate(BaseModel):
    title: str
    content: str
    atom_type: str = "concept"
    context: str = ""
    source: str = ""
    author: str = "System"
    metadata: Dict[str, Any] = {}

class AtomUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    atom_type: Optional[str] = None
    context: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RelationCreate(BaseModel):
    from_atom_id: str
    to_atom_id: str
    relation_type: str
    strength: float = 1.0

class SourceCreate(BaseModel):
    title: str
    content: str = ""
    file_path: str = ""


# ============ HEALTH CHECK & ROOT ============

@app.get("/", response_class=HTMLResponse)
async def root():
    """Trang chủ - Hero Box"""
    return hero_box.render()

@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái hệ thống"""
    db = get_db()
    atoms_count = len(db.get_all_atoms())
    return {
        "status": "healthy",
        "version": "2.0.0",
        "atoms_count": atoms_count,
        "timestamp": datetime.now().isoformat()
    }


# ============ SMART BOXES ROUTES ============

@app.get("/intelligence-core", response_class=HTMLResponse)
async def intelligence_core():
    """Intelligence Core Box"""
    return intelligence_box.render()

@app.get("/living-book", response_class=HTMLResponse)
async def living_book():
    """Living Book Box - Knowledge Graph visualization"""
    return living_book_box.render()

@app.get("/atom-manager", response_class=HTMLResponse)
async def atom_manager():
    """Atom Manager Box - Quản lý Knowledge Atoms"""
    return atom_manager_box.render()

@app.get("/chat-widget", response_class=HTMLResponse)
async def chat_widget():
    """AI Chat Widget"""
    return chat_widget_box.render()


# ============ ATOMS CRUD API ============

@app.get("/api/atoms")
async def get_all_atoms():
    """Lấy tất cả Knowledge Atoms"""
    db = get_db()
    return db.get_all_atoms()

@app.get("/api/atoms/{atom_id}")
async def get_atom(atom_id: str):
    """Lấy thông tin một Atom theo ID"""
    db = get_db()
    atom = db.get_atom(atom_id)
    if not atom:
        raise HTTPException(status_code=404, detail="Atom not found")
    return atom

@app.post("/api/atoms")
async def create_atom(atom: AtomCreate):
    """Tạo Knowledge Atom mới"""
    db = get_db()
    atom_id = db.create_atom({
        "title": atom.title,
        "content": atom.content,
        "atom_type": atom.atom_type,
        "context": atom.context,
        "source": atom.source,
        "author": atom.author,
        "metadata": atom.metadata
    })
    return {"atom_id": atom_id, "status": "created"}

@app.put("/api/atoms/{atom_id}")
async def update_atom(atom_id: str, updates: AtomUpdate):
    """Cập nhật Atom"""
    db = get_db()
    update_dict = {k: v for k, v in updates.dict().items() if v is not None}
    success = db.update_atom(atom_id, update_dict)
    if not success:
        raise HTTPException(status_code=404, detail="Atom not found")
    return {"status": "updated"}

@app.delete("/api/atoms/{atom_id}")
async def delete_atom(atom_id: str):
    """Xóa Atom"""
    db = get_db()
    success = db.delete_atom(atom_id)
    if not success:
        raise HTTPException(status_code=404, detail="Atom not found")
    return {"status": "deleted"}


# ============ RELATIONS API ============

@app.get("/api/relations/{atom_id}")
async def get_relations(atom_id: str):
    """Lấy tất cả relations của một atom"""
    db = get_db()
    return db.get_relations_for_atom(atom_id)

@app.post("/api/relations")
async def create_relation(relation: RelationCreate):
    """Tạo relation giữa 2 atoms"""
    db = get_db()
    relation_id = db.create_relation(
        relation.from_atom_id,
        relation.to_atom_id,
        relation.relation_type,
        relation.strength
    )
    return {"relation_id": relation_id, "status": "created"}

@app.get("/api/graph")
async def get_graph_data():
    """Lấy dữ liệu Knowledge Graph"""
    db = get_db()
    return db.get_graph_data()


# ============ SOURCES API ============

@app.get("/api/sources")
async def get_all_sources():
    """Lấy tất cả sources"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources ORDER BY upload_date DESC")
    sources = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sources

@app.post("/api/sources")
async def create_source(source: SourceCreate):
    """Tạo source mới"""
    db = get_db()
    source_id = f"SRC-{uuid.uuid4().hex[:8]}"
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sources (source_id, title, content, file_path, upload_date, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        source_id,
        source.title,
        source.content,
        source.file_path,
        datetime.now().isoformat(),
        json.dumps({})
    ))
    conn.commit()
    conn.close()
    return {"source_id": source_id, "status": "created"}


# ============ FILE UPLOAD & PARSING ============

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file (PDF, DOCX, TXT) và parse thành Knowledge Atoms"""
    # Tạo thư mục uploads nếu chưa có
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Lưu file
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_id = uuid.uuid4().hex[:8]
    file_path = os.path.join(uploads_dir, f"{file_id}{file_ext}")
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Parse file thành atoms
    try:
        atoms = parser.parse_file(file_path)
        
        # Lưu atoms vào database
        db = get_db()
        created_ids = []
        for atom_data in atoms:
            atom_id = db.create_atom(atom_data)
            created_ids.append(atom_id)
        
        return {
            "status": "success",
            "file": file.filename,
            "atoms_created": len(created_ids),
            "atom_ids": created_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")


@app.post("/api/parse-text")
async def parse_text(text: str = Form(...), title: str = Form("Untitled")):
    """Parse text trực tiếp thành Knowledge Atoms"""
    try:
        atoms = parser.parse_text(text, title=title)
        
        db = get_db()
        created_ids = []
        for atom_data in atoms:
            atom_id = db.create_atom(atom_data)
            created_ids.append(atom_id)
        
        return {
            "status": "success",
            "atoms_created": len(created_ids),
            "atom_ids": created_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")


# ============ AI ANALYSIS ENDPOINTS ============

@app.post("/api/atoms/analyze")
async def analyze_atom(atom_id: str, provider: str = "ollama"):
    """Phân tích một atom bằng AI"""
    try:
        analyzer = get_analyzer(provider)
        db = get_db()
        
        atom = db.get_atom(atom_id)
        if not atom:
            raise HTTPException(status_code=404, detail="Atom not found")
        
        analysis = analyzer.analyze_atom(
            content=atom.get('content', ''),
            title=atom.get('title', '')
        )
        
        db.update_atom(atom_id, {
            "ai_analysis": analysis,
            "analyzed_at": datetime.now().isoformat()
        })
        
        return {
            "atom_id": atom_id,
            "analysis": analysis,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in analyze_atom: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/atoms/batch-analyze")
async def batch_analyze_atoms(provider: str = "ollama"):
    """Phân tích tất cả atoms chưa được phân tích"""
    try:
        analyzer = get_analyzer(provider)
        db = get_db()
        
        atoms = db.get_all_atoms()
        unanalyzed = [a for a in atoms if not a.get('ai_analysis')]
        
        if not unanalyzed:
            return {"message": "All atoms are already analyzed", "analyzed_count": 0}
        
        results = analyzer.batch_analyze(unanalyzed)
        
        for result in results:
            atom_id = result.pop('atom_id', None)
            if atom_id:
                db.update_atom(atom_id, {
                    "ai_analysis": result,
                    "analyzed_at": datetime.now().isoformat()
                })
        
        return {
            "analyzed_count": len(results),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/atoms/{atom_id}/analysis")
async def get_atom_analysis(atom_id: str):
    """Lấy kết quả phân tích AI của một atom"""
    db = get_db()
    atom = db.get_atom(atom_id)
    if not atom:
        raise HTTPException(status_code=404, detail="Atom not found")
    
    return {
        "atom_id": atom_id,
        "analysis": atom.get('ai_analysis', {}),
        "analyzed_at": atom.get('analyzed_at')
    }


# ============ CHATBOT API (Placeholder) ============

@app.post("/api/chat")
async def chat(message: str = Form(...), context: Optional[str] = Form(None)):
    """AI Chat endpoint (cần tích hợp thêm LLM)"""
    return {
        "response": "Chat feature is under development. Please integrate with your preferred LLM.",
        "received": message
    }

# ============ ALIAS ENDPOINT cho Atom Manager UI ============

@app.post("/api/atoms/parse-file")
async def parse_file_endpoint(file: UploadFile = File(...)):
    """Alias endpoint cho Atom Manager UI"""
    # Tạo thư mục uploads nếu chưa có
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Lưu file
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_id = uuid.uuid4().hex[:8]
    file_path = os.path.join(uploads_dir, f"{file_id}{file_ext}")
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Parse file thành atoms
    try:
        atoms = parser.parse_file(file_path)
        
        # Lưu atoms vào database
        db = get_db()
        created_ids = []
        for atom_data in atoms:
            atom_id = db.create_atom(atom_data)
            created_ids.append(atom_id)
        
        return {
            "status": "success",
            "file": file.filename,
            "atoms_created": len(created_ids),
            "atom_ids": created_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parse error: {str(e)}")

    # ============ ALIAS ENDPOINT cho Atom Manager UI ============

@app.post("/api/atoms/parse-file")
async def parse_file_endpoint(file: UploadFile = File(...)):
    """Alias endpoint cho Atom Manager UI"""
    try:
        # Tạo thư mục uploads nếu chưa có
        uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Lưu file
        file_ext = os.path.splitext(file.filename)[1].lower()
        file_id = uuid.uuid4().hex[:8]
        file_path = os.path.join(uploads_dir, f"{file_id}{file_ext}")
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Parse file thành atoms
        atoms = parser.parse_file(file_path)
        
        # Lưu atoms vào database
        db = get_db()
        created_ids = []
        for atom_data in atoms:
            atom_id = db.create_atom(atom_data)
            created_ids.append(atom_id)
        
        return {
            "status": "success",
            "file": file.filename,
            "atoms_created": len(created_ids),
            "atom_ids": created_ids,
            "message": f"Đã tạo {len(created_ids)} Knowledge Atoms từ file {file.filename}"
        }
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"ERROR in parse_file: {error_detail}")
        return {
            "status": "error",
            "message": str(e),
            "detail": error_detail
        }


# ============ ENTRY POINT ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=55118)