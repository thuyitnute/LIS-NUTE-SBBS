from typing import Dict, Any

class LISHeroBox:
    def __init__(self):
        self.box_id = "SBBox-LIS-Hero-001"
        self.version = "1.0.0"
    
    def render(self, config: Dict[str, Any] = None) -> str:
        if config is None: config = {}
        
        slogan = config.get("slogan", "KIẾN TẠO - CHUẨN MỰC")
        subtitle = config.get("subtitle", "Learning Intelligence Infrastructure")
        description = config.get("description", "Hạ tầng trí tuệ cho Đại học AI-Native")
        cta_text = config.get("cta_text", "KHÁM PHÁ LIS")
        cta_link = config.get("cta_link", "/#vision")
        
        return f"""
        <style>
            .hero-container {{ position: relative; height: 100vh; width: 100%; background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 50%, #0d2137 100%); overflow: hidden; display: flex; flex-direction: column; }}
            .bg-layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('/static/background.png'); background-size: cover; background-position: center; opacity: 0.25; z-index: 1; }}
            .neural-network {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; opacity: 0.4; pointer-events: none; }}
            .node {{ position: absolute; width: 6px; height: 6px; background: #00d4ff; border-radius: 50%; box-shadow: 0 0 15px #00d4ff; animation: pulse 2s infinite; }}
            @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; transform: scale(1.2); }} }}
            .header {{ position: relative; z-index: 10; display: flex; justify-content: space-between; align-items: center; padding: 12px 40px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255, 255, 255, 0.1); flex-shrink: 0; height: 70px; }}
            .logo-container {{ display: flex; align-items: center; gap: 12px; }}
            .logo {{ width: 45px; height: 45px; border-radius: 50%; object-fit: cover; }}
            .logo-text {{ color: white; font-weight: 700; font-size: 1.1rem; }}
            .nav-menu {{ display: flex; gap: 25px; list-style: none; }}
            .nav-menu a {{ color: white; text-decoration: none; font-size: 13px; }}
            .login-btn {{ background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.3); color: white; padding: 8px 20px; border-radius: 25px; cursor: pointer; font-size: 13px; }}
            .main-content {{ position: relative; z-index: 10; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: 1; padding: 20px; text-align: center; min-height: 0; }}
            .lis-title {{ font-size: 5rem; font-weight: 900; color: white; text-shadow: 0 0 30px rgba(0, 212, 255, 0.8); margin-bottom: 5px; line-height: 1; }}
            .subtitle {{ font-size: 1.1rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 10px; letter-spacing: 2px; }}
            .slogan {{ font-size: 2.8rem; font-weight: 800; color: #ffd700; margin-bottom: 10px; line-height: 1.2; }}
            .description {{ font-size: 1.1rem; color: rgba(255, 255, 255, 0.8); margin-bottom: 20px; max-width: 700px; }}
            .cta-button {{ display: inline-block; padding: 14px 45px; background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); color: white; text-decoration: none; border-radius: 50px; font-size: 1.1rem; font-weight: 700; box-shadow: 0 10px 40px rgba(0, 212, 255, 0.5); }}
            .feature-cards {{ position: relative; z-index: 10; display: flex; justify-content: center; gap: 20px; padding: 0 20px 25px; flex-shrink: 0; }}
            .feature-card {{ background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 12px; padding: 15px 25px; color: white; text-align: center; min-width: 180px; }}
            .feature-icon {{ font-size: 1.5rem; margin-bottom: 5px; }}
            .feature-title {{ font-size: 0.95rem; font-weight: 600; }}
        </style>
        <div class="hero-container">
            <div class="bg-layer"></div>
            <div class="neural-network">
                <div class="node" style="top: 20%; left: 15%;"></div>
                <div class="node" style="top: 40%; left: 25%; animation-delay: 0.5s;"></div>
                <div class="node" style="top: 60%; left: 20%; animation-delay: 1s;"></div>
                <div class="node" style="top: 30%; right: 20%; animation-delay: 0.3s;"></div>
            </div>
            <header class="header">
                <div class="logo-container">
                    <img src="/static/logo.jpg" alt="NUTE Logo" class="logo">
                    <span class="logo-text">LIS</span>
                </div>
                <ul class="nav-menu">
                    <li><a href="/">Trang chủ</a></li>
                    <li><a href="/about">Giới thiệu LIS</a></li>
                    <li><a href="/ecosystem">Hệ sinh thái</a></li>
                </ul>
                <button class="login-btn">Login</button>
            </header>
            <div class="main-content">
                <h1 class="lis-title">LIS</h1>
                <h2 class="subtitle">{subtitle}</h2>
                <h3 class="slogan">{slogan}</h3>
                <p class="description">{description}</p>
                <a href="{cta_link}" class="cta-button">{cta_text} →</a>
            </div>
            <div class="feature-cards">
                <div class="feature-card"><div class="feature-icon">🎓</div><div class="feature-title">Đào tạo AI-Native</div></div>
                <div class="feature-card"><div class="feature-icon">🔬</div><div class="feature-title">Nghiên cứu & Đổi mới</div></div>
                <div class="feature-card"><div class="feature-icon">🌐</div><div class="feature-title">Cộng đồng Tri thức</div></div>
            </div>
        </div>
        """