"""
SBBox_Atom_Manager - Atom Manager Smart Box
"""

import os
from typing import Dict, Any


class AtomManagerBox:
    def render(self, config: Dict[str, Any] = None) -> str:
        # Đọc file HTML từ thư mục templates
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'atom_manager.html')
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()