from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import auth, user, chat, media, system, weather, admin
from app.database import init_db

# 创建 FastAPI 应用实例
app = FastAPI(
    title="ClassNet API",
    description="ClassNet 后端 API 服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/user", tags=["用户"])
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])
app.include_router(media.router, prefix="/api/media", tags=["媒体"])
app.include_router(system.router, prefix="/api/system", tags=["系统"])
app.include_router(weather.router, prefix="/api/weather", tags=["天气"])
app.include_router(admin.router, prefix="/api/admin", tags=["后台管理"])

# 初始化数据库
init_db()

# 静态文件服务 - 确保在 API 路由之后挂载
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")
    
    # 根路径重定向到前端
    @app.get("/")
    async def root():
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/frontend/auth/index.html")

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "ClassNet API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)