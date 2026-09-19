import json
import os
from datetime import datetime

class ConfigWire:
    """
    Smart Wire: Lớp kết nối thông minh.
    Nhiệm vụ: Fetch (Lấy dữ liệu) -> Validate (Kiểm tra) -> Transform (Chuyển đổi ngữ cảnh).
    """
    def __init__(self, config_file):
        self.config_file = config_file

    def fetch_and_transform(self):
        # 1. Fetch & Validate: Đọc file an toàn
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, self.config_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        except Exception as e:
            return {"error": str(e)}

        # 2. Transform (Context Translation): Thêm ngữ cảnh thời gian thực mà Box không cần tự lấy
        raw_data['current_time'] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        
        # 3. Security/Traceability: Đóng dấu nguồn gốc dữ liệu
        raw_data['wire_signature'] = "Secure-Wire-v1.0" 
        
        return raw_data