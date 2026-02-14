from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.config import settings
from app.api import auth, media, chat, weather, system, config, user
from app.database import init_db

# 初始化数据库
init_db()

app = FastAPI(
    title="ClassNet API",
    description="班级内部网络系统API",
    version="1.0.0"
)

# 获取项目根路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取前端静态文件路径
frontend_path = os.path.join(project_root, "frontend")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # 使用配置中的CORS origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加强缓存禁用中间件
@app.middleware("http")
async def disable_cache(request, call_next):
    response = await call_next(request)
    # 添加强缓存禁用头
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/user", tags=["用户"])
app.include_router(media.router, prefix="/api/media", tags=["媒体"])
app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])
app.include_router(weather.router, prefix="/api/weather", tags=["天气"])
app.include_router(system.router, prefix="/api/system", tags=["系统"])
app.include_router(config.router, prefix="/api/config", tags=["配置"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 挂载前端静态文件
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# 挂载根路径到项目根目录
app.mount("/", StaticFiles(directory=project_root, html=True), name="root")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
