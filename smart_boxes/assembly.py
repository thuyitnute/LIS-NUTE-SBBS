import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

from SBBox_LIS_Hero.box import LISHeroBox
from SBBox_Intelligence_Core.box import IntelligenceCoreBox
from SBBox_AI_Chat_Widget.box import AIChatWidgetBox
from SBBox_Living_Book.box import LivingBookBox
from SBBox_Atom_Manager.box import AtomManagerBox  # <-- Import box mới
from smart_wire import ConfigWire

class LISHomeAssembly:
    def __init__(self):
        self.boxes = {
            "hero": LISHeroBox(),
            "core": IntelligenceCoreBox(),
            "living_book": LivingBookBox(),
            "atom_manager": AtomManagerBox(),  # <-- Thêm box mới
            "chat_widget": AIChatWidgetBox()
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
            "living_book": {},
            "atom_manager": {},
            "chat_widget": {}
        }

    def render(self) -> str:
        hero_html = self.boxes["hero"].render(self.configurations["hero"])
        core_html = self.boxes["core"].render(self.configurations["core"])
        living_book_html = self.boxes["living_book"].render(self.configurations["living_book"])
        atom_manager_html = self.boxes["atom_manager"].render(self.configurations["atom_manager"])
        chat_html = self.boxes["chat_widget"].render(self.configurations["chat_widget"])
        
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
            {living_book_html}
            {atom_manager_html}
            {chat_html}
        </body>
        </html>
        """