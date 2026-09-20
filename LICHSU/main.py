import os, sys, io
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2, docx

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

from assembly import LISHomeAssembly
from database import KnowledgeDatabase
from atomic_parser import RuleBasedAtomicParser

app = FastAPI(title="LIS - SBBS", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

STATIC_DIR = os.path.join(current_dir, "static")
if not os.path.exists(STATIC_DIR): os.makedirs(STATIC_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

home_assembly = LISHomeAssembly()
db = KnowledgeDatabase()
parser = RuleBasedAtomicParser()

class ParseRequest(BaseModel):
    title: str
    content: str

@app.get("/", response_class=HTMLResponse)
def read_root(): return home_assembly.render()

@app.get("/api/health")
def health_check():
    return {"system": "LIS", "architecture": "SBBS", "version": "2.0", "status": "running"}

@app.post("/api/atoms/parse")
def parse_content(request: ParseRequest):
    try:
        atoms, relations = parser.parse_text(request.content, request.title)
        for atom in atoms: db.create_atom(atom)
        for rel in relations: db.create_relation(rel['from_atom_id'], rel['to_atom_id'], rel['relation_type'], 0.9)
        return {"success": True, "atom_count": len(atoms), "relation_count": len(relations), "message": "Thành công"}
    except Exception as e: return {"success": False, "error": str(e)}

@app.post("/api/atoms/parse-file")
async def parse_file_upload(file: UploadFile = File(...), title: str = ""):
    try:
        filename = file.filename.lower() if file.filename else ""
        content, file_type, raw_bytes = "", "", b""
        if filename.endswith('.txt'):
            file_type = "text/plain"; raw_bytes = await file.read(); content = raw_bytes.decode('utf-8', errors='ignore')
        elif filename.endswith('.pdf'):
            file_type = "application/pdf"; raw_bytes = await file.read()
            for page in PyPDF2.PdfReader(io.BytesIO(raw_bytes)).pages:
                if text := page.extract_text(): content += text + "\n\n"
        elif filename.endswith('.docx'):
            file_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"; raw_bytes = await file.read()
            for para in docx.Document(io.BytesIO(raw_bytes)).paragraphs:
                if para.text.strip(): content += para.text + "\n\n"
        else: return {"success": False, "error": "Chỉ hỗ trợ .txt, .pdf, .docx"}
        
        if not content.strip(): return {"success": False, "error": "File không có nội dung văn bản"}
        
        doc_title = title.strip() if title.strip() else file.filename
        atoms, relations = parser.parse_text(content, doc_title)
        for atom in atoms: db.create_atom(atom)
        for rel in relations: db.create_relation(rel['from_atom_id'], rel['to_atom_id'], rel['relation_type'], 0.9)
        
        return {"success": True, "atom_count": len(atoms), "relation_count": len(relations), "filename": file.filename, "file_size": len(raw_bytes)}
    except Exception as e: return {"success": False, "error": str(e)}

@app.get("/api/atoms")
def get_all_atoms(): return db.get_all_atoms()

@app.get("/api/atoms/{atom_id}")
def get_atom(atom_id: str):
    atom = db.get_atom(atom_id)
    return atom if atom else {"error": "Not found"}

@app.get("/api/graph/data")
def get_graph_data(): return db.get_graph_data()