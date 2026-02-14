from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import time
import asyncio
import mimetypes
import gzip
from app.config import settings

app = FastAPI(
    title="ClassNet Resource Server",
    description="媒体文件传输服务器",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
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

# 获取媒体目录的绝对路径
# 直接使用项目根目录下的data/media
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
media_dir = os.path.join(project_root, "..", "data", "media")
media_dir = os.path.abspath(media_dir)

# 确保媒体目录存在
os.makedirs(media_dir, exist_ok=True)

# 带宽限制配置（字节/秒）
BANDWIDTH_LIMIT = 1024 * 1024  # 1MB/s

# 打印调试信息
print(f"媒体目录: {media_dir}")
print(f"媒体目录是否存在: {os.path.exists(media_dir)}")
print(f"测试文件是否存在: {os.path.exists(os.path.join(media_dir, 'test.txt'))}")

@app.get("/")
def root():
    return {"message": "ClassNet Resource Server"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/media/{file_path:path}")
async def get_media(request: Request, file_path: str):
    """获取媒体文件（支持断点续传、Gzip压缩和带宽限制）"""
    # 构建完整的文件路径
    full_path = os.path.join(media_dir, file_path)
    
    # 打印调试信息
    print(f"请求文件: {file_path}")
    print(f"完整路径: {full_path}")
    print(f"文件是否存在: {os.path.exists(full_path)}")
    
    # 检查文件是否存在
    if not os.path.exists(full_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文件不存在: {full_path}"
        )
    
    # 检查是否是文件
    if not os.path.isfile(full_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="路径不是文件"
        )
    
    # 获取文件大小
    file_size = os.path.getsize(full_path)
    
    # 获取文件MIME类型
    mime_type, _ = mimetypes.guess_type(full_path)
    if mime_type is None:
        mime_type = "application/octet-stream"
    
    # 处理断点续传
    range_header = request.headers.get("range")
    start = 0
    end = file_size - 1
    
    if range_header:
        try:
            # 解析Range头
            range_val = range_header.split("=")[1]
            start_str, end_str = range_val.split("-")
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
            
            # 验证范围
            if start < 0 or end >= file_size or start > end:
                raise ValueError("Invalid range")
        except:
            # 无效的Range头，返回整个文件
            range_header = None
    
    # 计算要发送的字节数
    content_length = end - start + 1
    
    # 构建响应头
    headers = {
        "Content-Type": mime_type,
        "Content-Disposition": f"inline; filename*=UTF-8''{os.path.basename(full_path)}",
        "Accept-Ranges": "bytes",
        "Etag": f"{file_size}-{os.path.getmtime(full_path)}",
    }
    
    # 检查是否支持Gzip压缩
    accept_encoding = request.headers.get("accept-encoding", "")
    support_gzip = "gzip" in accept_encoding.lower()
    
    # 如果是断点续传，设置响应状态码和Content-Range头
    if range_header:
        status_code = status.HTTP_206_PARTIAL_CONTENT
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
    else:
        status_code = status.HTTP_200_OK
    
    # 自定义响应类，支持带宽限制和Gzip压缩
    async def file_stream():
        with open(full_path, "rb") as f:
            # 移动到起始位置
            f.seek(start)
            
            # 发送数据，支持带宽限制
            bytes_sent = 0
            chunk_size = 8192  # 8KB chunks
            start_time = time.time()
            
            while bytes_sent < content_length:
                # 计算当前chunk大小
                remaining = content_length - bytes_sent
                current_chunk_size = min(chunk_size, remaining)
                
                # 读取chunk
                data = f.read(current_chunk_size)
                if not data:
                    break
                
                # 如果支持Gzip压缩，压缩数据
                if support_gzip:
                    import io
                    buf = io.BytesIO()
                    with gzip.GzipFile(fileobj=buf, mode="w") as gz:
                        gz.write(data)
                    data = buf.getvalue()
                    headers["Content-Encoding"] = "gzip"
                
                # 发送chunk
                yield data
                bytes_sent += current_chunk_size
                
                # 带宽限制
                if BANDWIDTH_LIMIT > 0:
                    # 计算应该等待的时间
                    elapsed_time = time.time() - start_time
                    expected_time = bytes_sent / BANDWIDTH_LIMIT
                    
                    if elapsed_time < expected_time:
                        # 需要等待
                        await asyncio.sleep(expected_time - elapsed_time)
    
    # 返回流式响应
    return StreamingResponse(
        content=file_stream(),
        status_code=status_code,
        headers=headers
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "resource_server.main:app",
        host=settings.server_host,
        port=settings.resource_server_port,
        reload=True
    )
