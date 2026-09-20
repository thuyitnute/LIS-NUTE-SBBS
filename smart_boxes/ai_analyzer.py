"""
AI-Powered Knowledge Atom Analyzer
Hỗ trợ: Ollama (local) hoặc Groq (cloud - miễn phí)
"""

import json
import os
import requests
from typing import Dict, List, Any


class AtomAnalyzer:
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.model = "llama-3.1-8b-instant"  # Groq free model
        
        if provider == "groq":
            # Lấy API key từ environment variable
            self.api_key = os.getenv("GROQ_API_KEY", "")
            self.base_url = "https://api.groq.com/openai/v1"
        else:  # ollama
            self.base_url = "http://localhost:11434"
            self.model = "qwen2.5:0.5b"

    def analyze_atom(self, content: str, title: str = "") -> Dict[str, Any]:
        prompt = f"""Bạn là hệ thống phân tích tri thức chuyên sâu. Hãy phân tích nguyên tử tri thức sau:

TIÊU ĐỀ: {title}

NỘI DUNG:
{content}

YÊU CẦU PHÂN TÍCH:
1. Trích xuất các khái niệm chính (concepts)
2. Xác định mối quan hệ giữa các khái niệm (relations) với loại: is-a, part-of, depends-on, related-to
3. Đánh giá độ khó: beginner, intermediate, hoặc advanced
4. Xác định kiến thức tiên quyết (prerequisites)
5. Tóm tắt ngắn gọn trong 2-3 câu
6. Trích xuất từ khóa quan trọng (keywords)

TRẢ LỜI THEO ĐỊNH DẠNG JSON (chỉ JSON, không giải thích thêm):
{{
    "concepts": ["khái niệm 1", "khái niệm 2"],
    "relations": [
        {{"from": "khái niệm A", "to": "khái niệm B", "type": "is-a"}}
    ],
    "difficulty": "beginner",
    "prerequisites": ["kiến thức cần trước"],
    "summary": "Tóm tắt ngắn",
    "keywords": ["từ khóa 1", "từ khóa 2"]
}}"""

        try:
            if self.provider == "groq" and self.api_key:
                # Gọi Groq API
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "Bạn là chuyên gia phân tích tri thức. Luôn trả về JSON hợp lệ."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )
                result = response.json()
                result_text = result["choices"][0]["message"]["content"].strip()
            else:
                # Fallback: Ollama local
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False},
                    timeout=120
                )
                result_text = response.json().get("response", "").strip()

            # Clean JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            analysis = json.loads(result_text)

            return {
                "concepts": analysis.get("concepts", []),
                "relations": analysis.get("relations", []),
                "difficulty": analysis.get("difficulty", "unknown"),
                "prerequisites": analysis.get("prerequisites", []),
                "summary": analysis.get("summary", ""),
                "keywords": analysis.get("keywords", [])
            }

        except Exception as e:
            return {
                "error": str(e),
                "concepts": [],
                "relations": [],
                "difficulty": "unknown",
                "prerequisites": [],
                "summary": "",
                "keywords": []
            }

    def batch_analyze(self, atoms: List[Dict]) -> List[Dict]:
        results = []
        for atom in atoms:
            result = self.analyze_atom(
                content=atom.get('content', ''),
                title=atom.get('title', '')
            )
            result['atom_id'] = atom.get('atom_id')
            results.append(result)
        return results


_analyzer_instance = None

def get_analyzer(provider: str = None) -> AtomAnalyzer:
    global _analyzer_instance
    if provider is None:
        provider = "groq" if os.getenv("GROQ_API_KEY") else "ollama"
    if _analyzer_instance is None:
        _analyzer_instance = AtomAnalyzer(provider=provider)
    return _analyzer_instance