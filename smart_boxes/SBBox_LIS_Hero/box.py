from typing import Dict, Any

class LISHeroBox:
    """
    SBBox-LIS-Hero-001
    Smart Box hiển thị Hero Section cho LIS Platform
    """
    
    def __init__(self):
        self.box_id = "SBBox-LIS-Hero-001"
        self.version = "1.0.0"
    
    def render(self, config: Dict[str, Any] = None) -> str:
        """
        Render hero section HTML - Fit 100vh
        """
        if config is None:
            config = {}
        
        slogan = config.get("slogan", "KIẾN TẠO - CHUẨN MỰC")
        subtitle = config.get("subtitle", "Learning Intelligence Infrastructure")
        description = config.get("description", "Hạ tầng trí tuệ cho Đại học AI-Native")
        cta_text = config.get("cta_text", "KHÁM PHÁ LIS")
        cta_link = config.get("cta_link", "/#vision")
        
        html = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LIS - NUTE</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                html, body {{
                    height: 100%;
                    overflow: hidden;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                
                .hero-container {{
                    position: relative;
                    height: 100vh;
                    width: 100%;
                    background: linear-gradient(135deg, #0a1628 0%, #1e3a5f 50%, #0d2137 100%);
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}
                
                /* Background Image Layer */
                .bg-layer {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-image: url('/static/background.png');
                    background-size: cover;
                    background-position: center;
                    opacity: 0.25;
                    z-index: 1;
                }}
                
                /* Neural Network Animation */
                .neural-network {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 2;
                    opacity: 0.4;
                    pointer-events: none;
                }}
                
                .node {{
                    position: absolute;
                    width: 6px;
                    height: 6px;
                    background: #00d4ff;
                    border-radius: 50%;
                    box-shadow: 0 0 15px #00d4ff, 0 0 30px #00d4ff;
                    animation: pulse 2s infinite;
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ opacity: 1; transform: scale(1); }}
                    50% {{ opacity: 0.5; transform: scale(1.2); }}
                }}
                
                /* Header - Cố định chiều cao */
                .header {{
                    position: relative;
                    z-index: 10;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 12px 40px;
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    flex-shrink: 0;
                    height: 70px;
                }}
                
                .logo-container {{
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }}
                
                .logo {{
                    width: 45px;
                    height: 45px;
                    border-radius: 50%;
                    object-fit: cover;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                }}
                
                .logo-text {{
                    color: white;
                    font-weight: 700;
                    font-size: 1.1rem;
                    letter-spacing: 1px;
                }}
                
                .nav-menu {{
                    display: flex;
                    gap: 25px;
                    list-style: none;
                }}
                
                .nav-menu a {{
                    color: white;
                    text-decoration: none;
                    font-size: 13px;
                    transition: color 0.3s;
                }}
                
                .nav-menu a:hover {{
                    color: #00d4ff;
                }}
                
                .login-btn {{
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    color: white;
                    padding: 8px 20px;
                    border-radius: 25px;
                    cursor: pointer;
                    transition: all 0.3s;
                    font-size: 13px;
                }}
                
                .login-btn:hover {{
                    background: rgba(255, 255, 255, 0.2);
                }}
                
                /* Main Content - Chiếm phần còn lại */
                .main-content {{
                    position: relative;
                    z-index: 10;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    flex: 1;
                    padding: 20px 20px 10px;
                    text-align: center;
                    min-height: 0;
                }}
                
                .lis-title {{
                    font-size: 5rem;
                    font-weight: 900;
                    color: white;
                    text-shadow: 0 0 30px rgba(0, 212, 255, 0.8),
                                 0 0 60px rgba(0, 212, 255, 0.6),
                                 0 0 90px rgba(0, 212, 255, 0.4);
                    margin-bottom: 5px;
                    line-height: 1;
                    animation: glow 3s ease-in-out infinite;
                }}
                
                @keyframes glow {{
                    0%, 100% {{ text-shadow: 0 0 30px rgba(0, 212, 255, 0.8), 0 0 60px rgba(0, 212, 255, 0.6); }}
                    50% {{ text-shadow: 0 0 40px rgba(0, 212, 255, 1), 0 0 80px rgba(0, 212, 255, 0.8), 0 0 120px rgba(0, 212, 255, 0.6); }}
                }}
                
                .subtitle {{
                    font-size: 1.1rem;
                    color: rgba(255, 255, 255, 0.9);
                    margin-bottom: 10px;
                    font-weight: 300;
                    letter-spacing: 2px;
                }}
                
                .slogan {{
                    font-size: 2.8rem;
                    font-weight: 800;
                    background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 10px;
                    line-height: 1.2;
                    animation: shimmer 3s infinite;
                }}
                
                @keyframes shimmer {{
                    0%, 100% {{ filter: brightness(1); }}
                    50% {{ filter: brightness(1.3); }}
                }}
                
                .description {{
                    font-size: 1.1rem;
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 20px;
                    max-width: 700px;
                    line-height: 1.4;
                }}
                
                .cta-button {{
                    display: inline-block;
                    padding: 14px 45px;
                    background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 50px;
                    font-size: 1.1rem;
                    font-weight: 700;
                    letter-spacing: 2px;
                    box-shadow: 0 10px 40px rgba(0, 212, 255, 0.5);
                    transition: all 0.3s;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                }}
                
                .cta-button:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 15px 50px rgba(0, 212, 255, 0.8);
                    background: linear-gradient(135deg, #00e5ff 0%, #00aadd 100%);
                }}
                
                /* Floating Elements */
                .floating-element {{
                    position: absolute;
                    z-index: 5;
                    opacity: 0.6;
                    animation: float 6s ease-in-out infinite;
                    pointer-events: none;
                }}
                
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                    50% {{ transform: translateY(-15px) rotate(5deg); }}
                }}
                
                .brain-icon {{
                    top: 25%;
                    left: 8%;
                    font-size: 3rem;
                }}
                
                .book-icon {{
                    top: 35%;
                    right: 8%;
                    font-size: 3rem;
                }}
                
                .atom-icon {{
                    bottom: 25%;
                    left: 12%;
                    font-size: 2.5rem;
                }}
                
                /* Feature Cards - Thu nhỏ và đặt sát dưới */
                .feature-cards {{
                    position: relative;
                    z-index: 10;
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    padding: 0 20px 25px;
                    flex-shrink: 0;
                }}
                
                .feature-card {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    padding: 15px 25px;
                    color: white;
                    text-align: center;
                    transition: all 0.3s;
                    min-width: 180px;
                    max-width: 220px;
                }}
                
                .feature-card:hover {{
                    background: rgba(255, 255, 255, 0.15);
                    transform: translateY(-3px);
                    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
                }}
                
                .feature-icon {{
                    font-size: 1.5rem;
                    margin-bottom: 5px;
                }}
                
                .feature-title {{
                    font-size: 0.95rem;
                    font-weight: 600;
                    line-height: 1.3;
                }}
            </style>
        </head>
        <body>
            <div class="hero-container">
                <!-- Background Layer -->
                <div class="bg-layer"></div>
                
                <!-- Neural Network Nodes -->
                <div class="neural-network">
                    <div class="node" style="top: 20%; left: 15%; animation-delay: 0s;"></div>
                    <div class="node" style="top: 40%; left: 25%; animation-delay: 0.5s;"></div>
                    <div class="node" style="top: 60%; left: 20%; animation-delay: 1s;"></div>
                    <div class="node" style="top: 30%; right: 20%; animation-delay: 0.3s;"></div>
                    <div class="node" style="top: 50%; right: 30%; animation-delay: 0.8s;"></div>
                    <div class="node" style="top: 70%; right: 25%; animation-delay: 1.2s;"></div>
                    <div class="node" style="top: 25%; left: 50%; animation-delay: 0.6s;"></div>
                    <div class="node" style="top: 65%; left: 45%; animation-delay: 1.1s;"></div>
                </div>
                
                <!-- Floating Elements -->
                <div class="floating-element brain-icon">🧠</div>
                <div class="floating-element book-icon"></div>
                <div class="floating-element atom-icon">⚛️</div>
                
                <!-- Header -->
                <header class="header">
                    <div class="logo-container">
                        <img src="/static/logo.jpg" alt="NUTE Logo" class="logo">
                        <span class="logo-text">LIS</span>
                    </div>
                    <ul class="nav-menu">
                        <li><a href="/">Trang chủ</a></li>
                        <li><a href="/about">Giới thiệu LIS</a></li>
                        <li><a href="/ecosystem">Hệ sinh thái</a></li>
                        <li><a href="/research">Nghiên cứu</a></li>
                        <li><a href="/training">Đào tạo</a></li>
                        <li><a href="/community">Cộng đồng</a></li>
                    </ul>
                    <button class="login-btn">Login</button>
                </header>
                
                <!-- Main Content -->
                <div class="main-content">
                    <h1 class="lis-title">LIS</h1>
                    <h2 class="subtitle">{subtitle}</h2>
                    <h3 class="slogan">{slogan}</h3>
                    <p class="description">{description}</p>
                    <a href="{cta_link}" class="cta-button">{cta_text} →</a>
                </div>
                
                <!-- Feature Cards -->
                <div class="feature-cards">
                    <div class="feature-card">
                        
                        <div class="feature-title">Đào tạo AI-Native</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon"></div>
                        <div class="feature-title">Nghiên cứu & Đổi mới</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon"></div>
                        <div class="feature-title">Cộng đồng Tri thức</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """
        Validate input configuration
        """
        if not config.get("slogan"):
            raise ValueError("INVALID_SLOGAN: Slogan cannot be empty")
        return True