from typing import Dict, Any

class IntelligenceCoreBox:
    def __init__(self):
        self.box_id = "SBBox-Intelligence-Core-002"
        self.version = "1.1.0" # Nâng version vì có thay đổi capability
    
    def render(self, config: Dict[str, Any] = None) -> str:
        # Nhận dữ liệu động từ Wire (nếu có)
        if config is None: config = {}
        
        dynamic_msg = config.get("dynamic_message", "Đang tải dữ liệu...")
        current_time = config.get("current_time", "--:--:--")
        wire_sig = config.get("wire_signature", "Unknown")
        status = config.get("system_status", "Offline")

        return f"""
        <style>
            .core-container {{ background: #050b14; padding: 60px 20px; text-align: center; color: white; position: relative; overflow: hidden; }}
            .live-status-bar {{ background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; border-radius: 8px; padding: 10px 20px; display: inline-flex; gap: 20px; margin-bottom: 40px; font-size: 0.9rem; font-family: monospace; }}
            .status-dot {{ width: 10px; height: 10px; background: #00ff88; border-radius: 50%; display: inline-block; animation: blink 1s infinite; }}
            @keyframes blink {{ 50% {{ opacity: 0.5; }} }}
            .core-title {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 40px; color: #00d4ff; text-transform: uppercase; letter-spacing: 2px; }}
            .core-grid {{ display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; max-width: 1200px; margin: 0 auto; }}
            .core-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 20px; padding: 30px 20px; width: 280px; transition: all 0.3s; }}
            .core-card:hover {{ transform: translateY(-10px); border-color: #00d4ff; box-shadow: 0 10px 40px rgba(0, 212, 255, 0.2); }}
            .core-icon {{ font-size: 3.5rem; margin-bottom: 15px; }}
            .core-card h3 {{ font-size: 1.3rem; margin-bottom: 10px; color: #ffd700; }}
            .core-card p {{ font-size: 0.95rem; color: rgba(255, 255, 255, 0.7); line-height: 1.5; }}
            .dynamic-msg {{ margin-top: 40px; font-style: italic; color: #00ff88; font-size: 1.1rem; }}
        </style>
        <div class="core-container">
            <!-- Thanh trạng thái nhận dữ liệu từ Smart Wire -->
            <div class="live-status-bar">
                <span><span class="status-dot"></span> {status}</span>
                <span>⏱ {current_time}</span>
                <span>🔒 {wire_sig}</span>
            </div>

            <h2 class="core-title">Hạt nhân Trí tuệ LIS</h2>
            <div class="core-grid">
                <div class="core-card">
                    <div class="core-icon">🧠</div>
                    <h3>Human Intelligence</h3>
                    <p>Con người là trung tâm. Sinh viên và Giảng viên đồng kiến tạo, điều phối dòng chảy tri thức.</p>
                </div>
                <div class="core-card">
                    <div class="core-icon">🤖</div>
                    <h3>AI Agent Intelligence</h3>
                    <p>AI là đối tác. Hỗ trợ suy luận, tạo sinh, tự động hóa và cá nhân hóa trải nghiệm học tập.</p>
                </div>
                <div class="core-card">
                    <div class="core-icon">️</div>
                    <h3>Knowledge Graph</h3>
                    <p>Vũ trụ tri thức. Các nguyên tử tri thức kết nối chặt chẽ, liên tục tái sinh và tiến hóa.</p>
                </div>
            </div>
            <div class="dynamic-msg">"{dynamic_msg}"</div>
        </div>
        """