# ClassNet 项目

[![GitHub stars](https://img.shields.io/github/stars/Nixuko-Nivis/ClassNet?style=for-the-badge)](https://github.com/Nixuko-Nivis/ClassNet/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Nixuko-Nivis/ClassNet?style=for-the-badge)](https://github.com/Nixuko-Nivis/ClassNet/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Nixuko-Nivis/ClassNet?style=for-the-badge)](https://github.com/Nixuko-Nivis/ClassNet/issues)
[![GitHub license](https://img.shields.io/github/license/Nixuko-Nivis/ClassNet?style=for-the-badge)](https://github.com/Nixuko-Nivis/ClassNet/blob/main/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/Nixuko-Nivis/ClassNet?style=for-the-badge)](https://github.com/Nixuko-Nivis/ClassNet)
[![GitHub language count](https://img.shields.io/github/languages/count/Nixuko-Nivis/ClassNet?style=for-the-badge)](https://github.com/Nixuko-Nivis/ClassNet)

## 项目介绍

ClassNet 是一个专为班级内部使用设计的网络系统，提供了丰富的功能，包括视频播放、音乐播放、日历、天气、AI聊天、聊天、课程表等应用。系统采用前后端分离的架构，后端使用 Python 构建 HTTP 服务器，前端使用 HTML、CSS 和 JavaScript 实现。

## 系统架构

- **前端**：HTML5, CSS3, JavaScript, Bulma组件库（优先使用）
- **后端**：Python 3.9+, FastAPI
- **数据库**：SQLite
- **认证**：JWT
- **缓存**：Redis
- **资源服务器**：独立的媒体文件传输服务

### 前端开发提示
- **优先使用Bulma**：在所有前端开发中，必须优先使用Bulma组件库，只有在Bulma无法满足需求时才进行自定义开发
- **AI开发提示**：当使用AI辅助开发时，直接要求使用Bulma组件库实现功能，无需额外说明
- **组件丰富**：Bulma提供了大量现成的组件，如按钮、卡片、表单、导航等，避免重复开发

## 主要功能

- **媒体资源管理**：支持视频、音频等媒体文件的浏览和访问
- **独立资源服务器**：提供高性能的媒体文件传输服务
- **资源搜索**：支持按文件名和类型搜索媒体资源
- **目录浏览**：提供直观的 HTML 目录浏览界面
- **用户认证**：支持用户注册、登录和密码修改
- **聊天系统**：支持私聊、群聊等功能，使用 WebSocket 实现实时通信
- **AI 集成**：集成了 AI 聊天功能，提供智能对话能力
- **天气服务**：提供实时天气信息
- **课程表管理**：支持查看和管理课程表

## 目录结构

```
Server-refactor/
├── backend/              # 后端代码
│   ├── app/              # 应用核心
│   │   ├── api/          # API路由
│   │   ├── services/     # 业务逻辑
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # 数据验证
│   │   ├── utils/        # 工具函数
│   │   ├── config.py     # 配置文件
│   │   └── __init__.py
│   ├── resource_server/  # 资源服务器
│   ├── main.py           # 主服务器入口
│   ├── requirements.txt  # 依赖文件
│   └── .env.example      # 环境变量示例
├── frontend/             # 前端代码
│   ├── auth/             # 认证相关
│   ├── desktop/          # 桌面应用
│   ├── public/           # 公共资源
│   │   ├── fontawesome/  # FontAwesome图标库
│   │   ├── bulma/        # Bulma组件库
│   │   ├── images/       # 图片资源
│   │   └── styles/       # 公共样式
│   └── apps/             # 各个应用
├── data/                 # 数据目录
│   ├── media/            # 媒体文件
│   └── database/         # 数据库文件
├── scripts/              # 脚本文件
├── README.md             # 项目说明
├── 开发文档.md            # 开发文档
└── 重构计划.md            # 重构计划
```

## 安装指南

### 前置要求

- Python 3.9+
- pip
- Redis (可选，用于缓存)

### 安装步骤

1. **克隆项目**

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   ```

3. **激活虚拟环境**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **安装依赖**
   ```bash
   pip install -r backend/requirements.txt
   ```

5. **配置环境变量**
   ```bash
   cp backend/.env.example backend/.env
   # 编辑 .env 文件，填写相应配置
   ```

6. **创建数据目录**
   ```bash
   mkdir -p data/media/videos data/media/audios data/media/photos data/database
   ```

## 运行项目

### 启动主服务器

```bash
python backend/main.py
```

### 启动资源服务器

```bash
python backend/resource_server/main.py
```

### 一键启动脚本

```bash
# Windows
scripts\start.bat

# Linux/Mac
chmod +x scripts/start.sh
./scripts/start.sh
```

## 访问地址

- **主服务器**：http://localhost:8000
- **资源服务器**：http://localhost:8001
- **API文档**：http://localhost:8000/docs

## 开发指南

### 代码规范

- **Python**：遵循 PEP 8 规范
- **JavaScript**：遵循 ES5/ES6 规范
- **命名约定**：
  - 类名：大驼峰命名法
  - 函数和变量名：小写字母加下划线
  - 常量：全大写字母加下划线

### 开发流程

1. **创建分支**：从 develop 分支创建功能分支
2. **开发功能**：在功能分支上开发
3. **提交代码**：使用规范的提交信息
4. **创建PR**：向 develop 分支创建 Pull Request
5. **代码审查**：团队成员审查代码
6. **合并分支**：审查通过后合并到 develop 分支

## 测试

### 运行单元测试

```bash
pytest backend/tests/
```

### 运行集成测试

```bash
pytest backend/tests/integration/
```

## 部署

### 生产环境部署

1. **构建项目**
   ```bash
   # Windows
   scripts\build.bat
   
   # Linux/Mac
   chmod +x scripts/build.sh
   ./scripts/build.sh
   ```

2. **启动服务**
   ```bash
   # Windows
   scripts\start.bat
   
   # Linux/Mac
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```

## 维护与监控

### 日志管理

- 主服务器日志：`backend/logs/server.log`
- 资源服务器日志：`backend/logs/resource_server.log`
- 访问日志：`backend/logs/access.log`

### 错误处理

系统实现了统一的错误处理机制，所有错误都会记录到日志文件中，并返回适当的错误响应。

### 定期维护

- 定期清理日志文件
- 定期备份数据库
- 定期更新依赖包

## 贡献指南

1. **Fork 项目**
2. **创建功能分支**
3. **提交更改**
4. **创建 Pull Request**

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请联系项目维护者。

---

**注意**：本系统仅用于班级内部使用，请勿用于生产环境。