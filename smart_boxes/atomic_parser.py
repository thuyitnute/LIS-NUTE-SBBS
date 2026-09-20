"""
Atomic Parser - Rule-based Structured Parser v2.0
Phân tích văn bản thành Knowledge Atoms
"""

import re
import uuid
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class AtomicParser:
    """
    Parser để phân tích văn bản thành Knowledge Atoms
    Sử dụng rule-based approach để trích xuất cấu trúc
    """
    
    def __init__(self):
        self.rules = {
            'concept': r'(?:khái niệm|định nghĩa|concept|definition)[:\s]+(.+?)(?=\n\n|\Z)',
            'principle': r'(?:nguyên lý|nguyên tắc|principle)[:\s]+(.+?)(?=\n\n|\Z)',
            'reasoning': r'(?:lập luận|lý do|reasoning|logic)[:\s]+(.+?)(?=\n\n|\Z)',
            'evidence': r'(?:bằng chứng|evidence|dẫn chứng)[:\s]+(.+?)(?=\n\n|\Z)',
            'question': r'(?:câu hỏi|question|thắc mắc)[:\s]+(.+?)(?=\n\n|\Z)',
        }
    
    def parse_text(self, text: str, title: str = "Untitled") -> List[Dict[str, Any]]:
        """
        Parse text thành danh sách Knowledge Atoms
        
        Returns:
            List[Dict]: Danh sách atoms với cấu trúc chuẩn
        """
        atoms = []
        
        # Tách text thành các đoạn
        sections = re.split(r'\n\s*\n', text.strip())
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            
            atom = self._parse_section(section, title, i)
            if atom:
                atoms.append(atom)
        
        # Nếu không parse được section nào, tạo 1 atom từ toàn bộ text
        if not atoms and text.strip():
            atoms.append({
                'atom_id': f"ATOM-{uuid.uuid4().hex[:8]}",
                'title': title,
                'content': text.strip(),
                'atom_type': 'concept',
                'context': '',
                'source': 'Manual Input',
                'author': 'System',
                'created_at': datetime.now().isoformat(),
                'metadata': {}
            })
        
        return atoms
    
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse file (TXT, PDF, DOCX) thành Knowledge Atoms
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Đọc file tùy theo định dạng
        if path.suffix.lower() == '.txt':
            content = path.read_text(encoding='utf-8')
        elif path.suffix.lower() == '.pdf':
            content = self._read_pdf(file_path)
        elif path.suffix.lower() in ['.docx', '.doc']:
            content = self._read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        title = path.stem
        return self.parse_text(content, title)
    
    def _parse_section(self, section: str, base_title: str, index: int) -> Dict[str, Any] | None:
        """Parse một section thành atom"""
        
        # Tìm loại atom
        atom_type = 'concept'
        for type_name, pattern in self.rules.items():
            if re.search(pattern, section, re.IGNORECASE):
                atom_type = type_name
                break
        
        # Trích xuất tiêu đề (dòng đầu tiên)
        lines = section.strip().split('\n')
        title = lines[0].strip() if lines else f"{base_title} - Part {index + 1}"
        
        # Loại bỏ các markers
        title = re.sub(r'^(?:#|\*|-|\d+\.)\s*', '', title)
        
        # Nếu title quá dài, cắt ngắn
        if len(title) > 200:
            title = title[:197] + "..."
        
        return {
            'atom_id': f"ATOM-{uuid.uuid4().hex[:8]}",
            'title': title,
            'content': section.strip(),
            'atom_type': atom_type,
            'context': '',
            'source': 'Parsed',
            'author': 'Parser',
            'created_at': datetime.now().isoformat(),
            'metadata': {
                'parsed_from': base_title,
                'section_index': index
            }
        }
    
    def _read_pdf(self, file_path: str) -> str:
        """Đọc nội dung file PDF"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
                return text
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF parsing. Install with: pip install PyPDF2")
    
    def _read_docx(self, file_path: str) -> str:
        """Đọc nội dung file DOCX"""
        try:
            from docx import Document
            doc = Document(file_path)
            return "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        except ImportError:
            raise ImportError("python-docx is required for DOCX parsing. Install with: pip install python-docx")


# Test parser
if __name__ == "__main__":
    parser = AtomicParser()
    
    test_text = """
# Khái niệm Infrastructure
    
Infrastructure là hạ tầng cơ bản để xây dựng hệ thống.

## Nguyên lý hoạt động

Infrastructure cần phải scalable và reliable.

## Bằng chứng

Các công ty lớn đều đầu tư mạnh vào infrastructure.
"""
    
    atoms = parser.parse_text(test_text, "Test Infrastructure")
    print(f"Parsed {len(atoms)} atoms:")
    for atom in atoms:
        print(f"  - {atom['title']} ({atom['atom_type']})")