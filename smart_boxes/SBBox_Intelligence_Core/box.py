from typing import Dict, Any

class IntelligenceCoreBox:
    def __init__(self):
        self.box_id = "SBBox-Intelligence-Core-002"
        self.version = "1.0.0"
    
    def render(self, config: Dict[str, Any] = None) -> str:
        return """
        <style>
            .core-container { background: #050b14; padding: 80px 20px; text-align: center; color: white; position: relative; overflow: hidden; }
            .core-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 50px; color: #00d4ff; text-transform: uppercase; letter-spacing: 2px; }
            .core-grid { display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; max-width: 1200px; margin: 0 auto; }
            .core-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 20px; padding: 40px 30px; width: 300px; transition: all 0.3s; position: relative; }
            .core-card:hover { transform: translateY(-10px); border-color: #00d4ff; box-shadow: 0 10px 40px rgba(0, 212, 255, 0.2); }
            .core-icon { font-size: 4rem; margin-bottom: 20px; }
            .core-card h3 { font-size: 1.5rem; margin-bottom: 15px; color: #ffd700; }
            .core-card p { font-size: 1rem; color: rgba(255, 255, 255, 0.7); line-height: 1.6; }
            .connection-line { position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #00d4ff, transparent); z-index: 0; opacity: 0.3; }
        </style>
        <div class="core-container">
            <div class="connection-line"></div>
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
                    <div class="core-icon">🕸️</div>
                    <h3>Knowledge Graph</h3>
                    <p>Vũ trụ tri thức. Các nguyên tử tri thức kết nối chặt chẽ, liên tục tái sinh và tiến hóa.</p>
                </div>
            </div>
        </div>
        """