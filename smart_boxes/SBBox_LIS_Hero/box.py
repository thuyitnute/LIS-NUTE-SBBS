from typing import Dict, Any

class HeroBox:
    """
    LIS Hero Box - Trang chủ giới thiệu hệ thống
    """
    
    def render(self, config: Dict[str, Any] = None) -> str:
        return """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LIS - Learning Intelligence Infrastructure</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center">
            <div class="text-center text-white px-4">
                <div class="mb-8">
                    <img src="/static/logo.jpg" alt="LIS Logo" class="w-32 h-32 mx-auto mb-6 rounded-full shadow-2xl" 
                         onerror="this.style.display='none'">
                    <h1 class="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                        LIS SBBS
                    </h1>
                    <p class="text-2xl text-gray-300 mb-2">Learning Intelligence Infrastructure</p>
                    <p class="text-xl text-gray-400 mb-8">Smart Black Box System</p>
                    <p class="text-lg text-gray-400 mb-12">Trường Đại học Sư phạm Kỹ thuật Nam Định</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto mb-12">
                    <a href="/intelligence-core" class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 hover:bg-opacity-20 transition-all transform hover:-translate-y-1">
                        <div class="text-4xl mb-3">🧠</div>
                        <h3 class="text-xl font-semibold mb-2">Intelligence Core</h3>
                        <p class="text-gray-300 text-sm">Trái tim AI của hệ thống</p>
                    </a>
                    
                    <a href="/living-book" class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 hover:bg-opacity-20 transition-all transform hover:-translate-y-1">
                        <div class="text-4xl mb-3">📚</div>
                        <h3 class="text-xl font-semibold mb-2">Living Book</h3>
                        <p class="text-gray-300 text-sm">Knowledge Graph tương tác</p>
                    </a>
                    
                    <a href="/atom-manager" class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 hover:bg-opacity-20 transition-all transform hover:-translate-y-1">
                        <div class="text-4xl mb-3">⚛️</div>
                        <h3 class="text-xl font-semibold mb-2">Atom Manager</h3>
                        <p class="text-gray-300 text-sm">Quản lý Knowledge Atoms</p>
                    </a>
                </div>
                
                <div class="text-sm text-gray-400">
                    <p>Phiên bản 2.0 - AI-Powered Knowledge Infrastructure</p>
                </div>
            </div>
        </body>
        </html>
        """