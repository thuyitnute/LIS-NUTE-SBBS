import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

from SBBox_LIS_Hero.box import LISHeroBox
from SBBox_Intelligence_Core.box import IntelligenceCoreBox
from SBBox_AI_Chat_Widget.box import AIChatWidgetBox # <-- Import Box mới
from smart_wire import ConfigWire

class LISHomeAssembly:
    def __init__(self):
        self.boxes = {
            "hero": LISHeroBox(),
            "core": IntelligenceCoreBox(),
            "chat_widget": AIChatWidgetBox() # <-- Đăng ký Box mới
        }
        
        self.data_wire = ConfigWire("context.json")
        dynamic_context = self.data_wire.fetch_and_transform()

        self.configurations = {
            "hero": {
                "slogan": "KIẾN TẠO - CHUẨN MỰC",
                "subtitle": "Learning Intelligence Infrastructure",
                "description": "Hạ tầng trí tuệ cho Đại học AI-Native",
                "cta_text": "KHÁM PHÁ LIS",
                "cta_link": "/#core"
            },
            "core": dynamic_context,
            "chat_widget": {} # Widget này hiện không cần config động
        }

    def render(self) -> str:
        # Render từng Box
        hero_html = self.boxes["hero"].render(self.configurations["hero"])
        core_html = self.boxes["core"].render(self.configurations["core"])
        chat_html = self.boxes["chat_widget"].render(self.configurations["chat_widget"]) # <-- Render Box mới
        
        # Lắp ráp vào khung xương
        return f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LIS - NUTE | Kiến tạo - Chuẩn mực</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; background: #050b14;">
            {hero_html}
            {core_html}
            {chat_html} <!-- Widget lơ lửng trên toàn bộ giao diện -->
        </body>
        </html>
        """