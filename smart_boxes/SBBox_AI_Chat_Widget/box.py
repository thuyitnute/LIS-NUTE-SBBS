from typing import Dict, Any

class AIChatWidgetBox:
    def __init__(self):
        self.box_id = "SBBox-AI-Chat-Widget-003"
        self.version = "1.0.0"
    
    def render(self, config: Dict[str, Any] = None) -> str:
        return """
        <style>
            .ai-widget-btn {
                position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px;
                background: linear-gradient(135deg, #00d4ff, #0099cc); border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 30px; color: white; cursor: pointer; z-index: 1000;
                box-shadow: 0 5px 20px rgba(0, 212, 255, 0.5); transition: transform 0.3s;
            }
            .ai-widget-btn:hover { transform: scale(1.1); }
            .ai-chat-window {
                position: fixed; bottom: 100px; right: 30px; width: 320px; height: 400px;
                background: rgba(10, 22, 40, 0.95); backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 15px;
                display: none; flex-direction: column; z-index: 1000; overflow: hidden;
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            }
            .chat-header {
                background: rgba(0, 212, 255, 0.2); padding: 15px; color: white;
                font-weight: bold; display: flex; justify-content: space-between; align-items: center;
            }
            .chat-body { flex: 1; padding: 15px; overflow-y: auto; color: #ccc; font-size: 0.9rem; }
            .ai-message { background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 10px; }
            .chat-input-area { padding: 10px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; }
            .chat-input { flex: 1; background: transparent; border: none; color: white; outline: none; padding: 5px; }
            .chat-send { background: #00d4ff; border: none; color: white; padding: 5px 15px; border-radius: 5px; cursor: pointer; }
        </style>

        <div class="ai-widget-btn" onclick="toggleChat()"></div>
        
        <div class="ai-chat-window" id="aiChatWindow">
            <div class="chat-header">
                <span>LIS AI Agent</span>
                <span style="cursor:pointer;" onclick="toggleChat()">✖</span>
            </div>
            <div class="chat-body" id="chatBody">
                <div class="ai-message">
                    Xin chào! Tôi là AI Agent của LIS. Tôi có thể giúp gì cho hành trình kiến tạo tri thức của bạn hôm nay?
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" placeholder="Nhập câu hỏi..." onkeypress="handleKeyPress(event)">
                <button class="chat-send" onclick="sendMessage()">Gửi</button>
            </div>
        </div>

        <script>
            function toggleChat() {
                const chat = document.getElementById('aiChatWindow');
                chat.style.display = chat.style.display === 'flex' ? 'none' : 'flex';
            }
            function sendMessage() {
                const input = document.querySelector('.chat-input');
                const body = document.getElementById('chatBody');
                if(input.value.trim() !== "") {
                    body.innerHTML += `<div style="text-align:right; margin-bottom:10px;"><span style="background:#0099cc; padding:10px; border-radius:10px; display:inline-block;">${input.value}</span></div>`;
                    input.value = "";
                    // Giả lập AI phản hồi
                    setTimeout(() => {
                        body.innerHTML += `<div class="ai-message">Tôi đã ghi nhận yêu cầu của bạn. Tính năng AI Reasoning đang được kết nối qua Smart Wire...</div>`;
                        body.scrollTop = body.scrollHeight;
                    }, 800);
                }
            }
            function handleKeyPress(e) { if(e.key === 'Enter') sendMessage(); }
        </script>
        """