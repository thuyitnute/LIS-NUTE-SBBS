import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class KnowledgeDatabase:
    """
    SQLite Database để lưu trữ Knowledge Atoms và Relations
    """
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Tạo connection đến database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Truy cập theo tên cột
        return conn
    
    def init_database(self):
        """Khởi tạo schema database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Bảng lưu Knowledge Atoms
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS atoms (
                atom_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                atom_type TEXT,
                concepts TEXT,
                principles TEXT,
                reasoning TEXT,
                evidence TEXT,
                socratic_questions TEXT,
                contradictions TEXT,
                context TEXT,
                source TEXT,
                author TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            )
        """)
        
        # Bảng lưu Relations giữa các Atoms
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                relation_id TEXT PRIMARY KEY,
                from_atom_id TEXT,
                to_atom_id TEXT,
                relation_type TEXT,
                strength REAL,
                created_at TEXT,
                FOREIGN KEY (from_atom_id) REFERENCES atoms(atom_id),
                FOREIGN KEY (to_atom_id) REFERENCES atoms(atom_id)
            )
        """)
        
        # Bảng lưu Sources (nguồn tài liệu gốc)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY,
                title TEXT,
                content TEXT,
                file_path TEXT,
                upload_date TEXT,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Đảm bảo có các cột mới cho AI analysis
        self._ensure_schema()
        
        print("✅ Database initialized successfully!")
    
    def _ensure_schema(self):
        """Đảm bảo schema có các cột cần thiết cho AI analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Thêm cột ai_analysis nếu chưa có
        try:
            cursor.execute("ALTER TABLE atoms ADD COLUMN ai_analysis TEXT")
        except:
            pass  # Cột đã tồn tại
        
        # Thêm cột analyzed_at nếu chưa có
        try:
            cursor.execute("ALTER TABLE atoms ADD COLUMN analyzed_at TEXT")
        except:
            pass  # Cột đã tồn tại
        
        conn.commit()
        conn.close()
    
    # ============ CRUD OPERATIONS FOR ATOMS ============
    
    def create_atom(self, atom_data: Dict[str, Any]) -> str:
        """Tạo một Knowledge Atom mới"""
        atom_id = atom_data.get('atom_id', f"ATOM-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO atoms (
                atom_id, title, content, atom_type, concepts, principles,
                reasoning, evidence, socratic_questions, contradictions,
                context, source, author, created_at, updated_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            atom_id,
            atom_data.get('title', ''),
            atom_data.get('content', ''),
            atom_data.get('atom_type', 'concept'),
            json.dumps(atom_data.get('concepts', [])),
            json.dumps(atom_data.get('principles', [])),
            json.dumps(atom_data.get('reasoning', [])),
            json.dumps(atom_data.get('evidence', [])),
            json.dumps(atom_data.get('socratic_questions', [])),
            json.dumps(atom_data.get('contradictions', [])),
            atom_data.get('context', ''),
            atom_data.get('source', ''),
            atom_data.get('author', 'System'),
            now,
            now,
            json.dumps(atom_data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
        
        return atom_id
    
    def get_atom(self, atom_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin một Atom theo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM atoms WHERE atom_id = ?", (atom_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            atom = dict(row)
            # Parse JSON fields
            if atom.get('ai_analysis'):
                try:
                    atom['ai_analysis'] = json.loads(atom['ai_analysis'])
                except:
                    atom['ai_analysis'] = {}
            if atom.get('metadata'):
                try:
                    atom['metadata'] = json.loads(atom['metadata'])
                except:
                    atom['metadata'] = {}
            return atom
        return None
    
    def get_all_atoms(self) -> List[Dict[str, Any]]:
        """Lấy tất cả Atoms"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM atoms ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        atoms = []
        for row in rows:
            atom = dict(row)
            # Parse JSON fields
            if atom.get('ai_analysis'):
                try:
                    atom['ai_analysis'] = json.loads(atom['ai_analysis'])
                except:
                    atom['ai_analysis'] = {}
            if atom.get('metadata'):
                try:
                    atom['metadata'] = json.loads(atom['metadata'])
                except:
                    atom['metadata'] = {}
            atoms.append(atom)
        
        return atoms
    
    def update_atom(self, atom_id: str, updates: Dict[str, Any]) -> bool:
        """Cập nhật Atom (hỗ trợ cả AI analysis)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra atom có tồn tại không
        cursor.execute("SELECT atom_id FROM atoms WHERE atom_id = ?", (atom_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        
        # Xử lý các trường đặc biệt (JSON)
        processed_updates = {}
        for key, value in updates.items():
            if key in ['ai_analysis', 'metadata', 'concepts', 'principles', 
                       'reasoning', 'evidence', 'socratic_questions', 'contradictions']:
                processed_updates[key] = json.dumps(value)
            else:
                processed_updates[key] = value
        
        # Thêm updated_at
        processed_updates['updated_at'] = datetime.now().isoformat()
        
        # Build SET clause
        set_clause = ', '.join([f"{key} = ?" for key in processed_updates.keys()])
        values = list(processed_updates.values()) + [atom_id]
        
        cursor.execute(f"""
            UPDATE atoms SET {set_clause} WHERE atom_id = ?
        """, values)
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def delete_atom(self, atom_id: str) -> bool:
        """Xóa Atom"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Xóa relations liên quan
        cursor.execute("DELETE FROM relations WHERE from_atom_id = ? OR to_atom_id = ?", 
                      (atom_id, atom_id))
        
        # Xóa atom
        cursor.execute("DELETE FROM atoms WHERE atom_id = ?", (atom_id,))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    # ============ RELATIONS OPERATIONS ============
    
    def create_relation(self, from_atom_id: str, to_atom_id: str, 
                       relation_type: str, strength: float = 1.0) -> str:
        """Tạo relation giữa 2 atoms"""
        import uuid
        relation_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO relations (relation_id, from_atom_id, to_atom_id, 
                                  relation_type, strength, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (relation_id, from_atom_id, to_atom_id, relation_type, 
              strength, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return relation_id
    
    def get_relations_for_atom(self, atom_id: str) -> List[Dict[str, Any]]:
        """Lấy tất cả relations của một atom"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM relations 
            WHERE from_atom_id = ? OR to_atom_id = ?
        """, (atom_id, atom_id))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_graph_data(self) -> Dict[str, Any]:
        """Lấy dữ liệu cho Knowledge Graph visualization"""
        atoms = self.get_all_atoms()
        
        nodes = []
        for atom in atoms:
            # Màu node dựa vào AI analysis
            color = '#3B82F6'  # Default blue
            if atom.get('ai_analysis'):
                difficulty = atom['ai_analysis'].get('difficulty', 'unknown')
                if difficulty == 'beginner':
                    color = '#10B981'  # Green
                elif difficulty == 'intermediate':
                    color = '#F59E0B'  # Orange
                elif difficulty == 'advanced':
                    color = '#EF4444'  # Red
            
            nodes.append({
                'id': atom['atom_id'],
                'title': atom['title'],
                'type': atom['atom_type'],
                'color': color,
                'analyzed': bool(atom.get('ai_analysis')),
                'label': atom['title'][:30] + '...' if len(atom['title']) > 30 else atom['title']
            })
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM relations")
        relations = cursor.fetchall()
        conn.close()
        
        links = []
        for rel in relations:
            links.append({
                'source': rel['from_atom_id'],
                'target': rel['to_atom_id'],
                'type': rel['relation_type'],
                'strength': rel['strength']
            })
        
        # Thêm relations từ AI analysis
        for atom in atoms:
            if atom.get('ai_analysis'):
                for rel in atom['ai_analysis'].get('relations', []):
                    links.append({
                        'source': rel.get('from', ''),
                        'target': rel.get('to', ''),
                        'type': rel.get('type', 'related-to'),
                        'strength': 0.5,
                        'from_ai': True
                    })
        
        return {'nodes': nodes, 'links': links}


# Singleton instance
_db_instance = None

def get_db() -> KnowledgeDatabase:
    """Lấy database instance (singleton)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = KnowledgeDatabase()
    return _db_instance