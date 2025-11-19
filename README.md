# 数据集共享平台 (Data-Web)

这是一个简洁、现代化的Web平台，旨在为科研人员或数据所有者提供一个渠道，用于在线发布、介绍并向注册用户提供数据集的下载。

本项目是根据用户需求，使用前后端分离架构从零开始构建的。

## ✨ 主要功能

- **用户系统**: 提供完整的用户注册和登录功能。
- **JWT 认证**: 使用 JSON Web Tokens (JWT) 对用户进行身份验证，保护核心数据接口。
- **数据集介绍**: 拥有一个公开的首页，用于详细展示数据集的背景、内容、格式和引用信息。
- **安全下载**: 用户登录后，可以访问受保护的页面，下载以 `.zip` 格式打包的完整数据集。
- **动态打包**: 后端采用动态打包机制，将服务器上的源数据实时压缩成ZIP文件供用户下载。

## 🛠️ 技术栈

本项目采用了当前流行且高效的技术栈：

- **后端 (Backend)**
  - **Python 3**: 核心编程语言。
  - **FastAPI**: 高性能的Web框架，自带交互式API文档。
  - **MongoDB**: 灵活的NoSQL数据库，用于存储用户信息。
  - **Motor**: 异步的MongoDB驱动，与FastAPI完美配合。
  - **Uvicorn**: ASGI服务器，用于运行FastAPI应用。
  - **Passlib & python-jose**: 用于密码哈希和JWT令牌的生成与验证。

- **前端 (Frontend)**
  - **Vue 3**: 渐进式的JavaScript框架。
  - **TypeScript**: 为JavaScript添加静态类型，提升代码健壮性。
  - **Vite**: 极速的下一代前端构建工具。
  - **Vue Router**: 官方的路由管理器。
  - **Pinia**: 官方推荐的状态管理库。
  - **Element Plus**: 成熟、美观的Vue 3组件库。
  - **Axios**: 用于与后端API进行网络通信。

## 📂 项目结构

项目采用前后端分离的单体仓库（monorepo）结构，清晰地划分了不同职责的代码。

```
data-web/
├── backend/         # FastAPI 后端应用
│   ├── app/         # 核心应用代码
│   ├── data/        # 存放原始数据集
│   └── venv/        # Python虚拟环境
├── frontend/        # Vue 3 前端应用
│   ├── src/         # 核心源代码
│   └── node_modules/# Node.js依赖
└── README.md        # 本文档
```

## 🚀 本地开发指南

请遵循以下步骤在您的本地环境中启动并运行本项目。

### 环境要求

- [Node.js](https://nodejs.org/) (v18+ recommended)
- [Python](https://www.python.org/) (v3.8+ recommended)
- [MongoDB](https://www.mongodb.com/try/download/community) (请确保MongoDB服务正在本地运行)

### 1. 启动后端服务

打开一个终端窗口：

```bash
# 1. 进入后端目录
cd backend

# 2. 创建并激活Python虚拟环境
# 在 Windows 上:
python -m venv venv
.\venv\Scripts\activate

# 在 macOS / Linux 上:
python3 -m venv venv
source venv/bin/activate

# 3. 安装所有Python依赖
pip install -r requirements.txt

# 4. 启动FastAPI应用
# 服务将运行在 http://127.0.0.1:8000
uvicorn app.main:app --reload
```
服务启动后，您可以访问 `http://127.0.0.1:8000/docs` 查看并测试所有后端API。

### 2. 启动前端服务

打开**另一个**终端窗口：

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装所有Node.js依赖
npm install

# 3. 启动Vite开发服务器
# 服务通常会运行在 http://localhost:5173
npm run dev
```

### 3. 访问应用

在浏览器中打开前端服务的地址 (例如 `http://localhost:5173`)，即可开始使用本平台。

## 📝 如何使用

1.  **放置数据**: 将您的病害图像和JSON描述文件放入 `backend/data/dataset_source/` 目录下。
2.  **访问首页**: 启动服务后，访问前端主页可看到数据集的介绍信息（信息可在 `backend/app/api/dataset_api.py` 中修改）。
3.  **注册与登录**: 点击“注册”创建一个新账户，然后使用该账户登录。
4.  **下载数据**: 登录成功后，您将被引导至数据下载页面，点击按钮即可下载 `dataset_source` 目录下的所有文件打包成的ZIP压缩包。

---
这份文档旨在帮助您或其他开发者快速理解并上手该项目。
