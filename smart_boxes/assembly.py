from SBBox_LIS_Hero.box import LISHeroBox
from SBBox_Intelligence_Core.box import IntelligenceCoreBox

class LISHomeAssembly:
    """
    Bộ điều phối lắp ráp trang chủ LIS.
    Khai báo kiến trúc hệ thống dưới dạng dữ liệu và lắp ráp các Smart Box.
    """
    def __init__(self):
        # Khởi tạo các Smart Box (Plug & Play)
        self.boxes = {
            "hero": LISHeroBox(),
            "core": IntelligenceCoreBox()
        }
        
        # Cấu hình cho từng Box (Data-driven)
        self.configurations = {
            "hero": {
                "slogan": "KIẾN TẠO - CHUẨN MỰC",
                "subtitle": "Learning Intelligence Infrastructure",
                "description": "Hạ tầng trí tuệ cho Đại học AI-Native",
                "cta_text": "KHÁM PHÁ LIS",
                "cta_link": "/#core"
            },
            "core": {} # Core box hiện tại chưa cần config
        }

    def render(self) -> str:
        """Lắp ráp và trả về toàn bộ HTML của trang chủ."""
        # Gọi render từng Box theo thứ tự lắp ráp
        hero_html = self.boxes["hero"].render(self.configurations["hero"])
        core_html = self.boxes["core"].render(self.configurations["core"])
        
        # Assembly đóng vai trò là "Khung xương" (Shell) bọc các mảnh ghép lại
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
        </body>
        </html>
        """