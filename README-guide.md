# 交通基础设施病害数据集网站 - 轻量级方案

## 一、核心思路

针对个人/实验室项目，建议采用 **轻量级实现** ，而非企业级大型系统。重点是快速上线，便于维护。

```
用户访问
    ↓
前端 (Vue 3 + TypeScript)
    ↓
后端 (FastAPI)
    ↓
数据库 (MongoDB)
    ↓
云存储 (本地服务器)

域名用阿里云的
```

---

## 二、推荐方案：FastAPI + Vue3 (极简版)

### 为什么选FastAPI而不是Django/Flask?

* **FastAPI** : 更适合API开发，启动快，自带数据验证，与Vue前端配合更灵活
* **对比Django** : Django过重，学习曲线陡，个人项目维护成本高
* **对比Flask** : Flask过轻，很多功能需要自己实现

### 项目规模

* **后端代码** : 500-1000行
* **前端代码** : 1000-1500行
* **数据库** : 3个集合表即可
* **部署** : 单台2核4GB服务器足够

---

## 三、后端极简架构 (FastAPI)

### 3.1 项目结构

```
backend/
├── app/
│   ├── main.py              # 应用主文件
│   ├── config.py            # 配置
│   ├── models.py            # 数据模型
│   ├── schemas.py           # 请求/响应模型
│   ├── database.py          # 数据库连接
│   ├── dependencies.py      # 依赖注入
│   ├── routers/
│   │   ├── auth.py          # 认证
│   │   ├── datasets.py      # 数据集管理
│   │   └── download.py      # 下载管理
│   └── utils/
│       ├── security.py      # JWT、密码加密
│       └── storage.py       # OSS操作
├── requirements.txt
├── Dockerfile
└── .env
```

### 3.2 核心代码示例

**main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, datasets, download

app = FastAPI(title="交通病害数据集平台")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(download.router)

@app.get("/health")
def health():
    return {"status": "ok"}
```

**models.py (MongoDB)**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password_hash: str
    created_at: datetime = datetime.now()

class Dataset(BaseModel):
    title: str
    description: str
    category: str  # "road_crack", "pothole", "bridge"
    image_count: int
    file_size: int  # bytes
    download_url: str  # OSS URL
    download_count: int = 0
    created_at: datetime = datetime.now()

class Download(BaseModel):
    user_id: str
    dataset_id: str
    download_time: datetime = datetime.now()
```

**auth.py (认证路由)**

```python
from fastapi import APIRouter, HTTPException
from datetime import timedelta
from app.utils.security import create_access_token, verify_password
from app import schemas

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def register(username: str, email: str, password: str):
    # 检查用户是否存在
    # 创建用户
    # 返回token
    pass

@router.post("/login")
async def login(email: str, password: str):
    # 验证用户
    # 返回token
    access_token = create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}
```

**datasets.py (数据集路由)**

```python
from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

@router.get("/")
async def list_datasets(skip: int = 0, limit: int = 20):
    # 分页获取数据集列表
    return {
        "total": 0,
        "datasets": []
    }

@router.get("/{dataset_id}")
async def get_dataset(dataset_id: str):
    # 获取数据集详情
    return {
        "id": dataset_id,
        "title": "",
        "description": "",
        "image_count": 0,
        "file_size": 0
    }

@router.post("/")
async def create_dataset(dataset: dict, current_user: str):
    # 创建新数据集(管理员)
    pass
```

### 3.3 数据库设计 (MongoDB)

```javascript
// users collection
{
  _id: ObjectId,
  username: String,
  email: String(unique),
  password_hash: String,
  role: String,  // "user", "admin"
  created_at: Date
}

// datasets collection
{
  _id: ObjectId,
  title: String,
  description: String,
  category: String,
  image_count: Number,
  file_size: Number,
  download_url: String,  // OSS/云存储URL
  download_count: Number,
  created_at: Date,
  metadata: {
    image_resolution: String,
    damage_types: [String],  // ["crack", "pothole"]
    collection_location: String
  }
}

// downloads collection
{
  _id: ObjectId,
  user_id: ObjectId,
  dataset_id: ObjectId,
  download_time: Date,
  file_size: Number
}
```

### 3.4 需要的依赖包

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pymongo==4.6.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
aiofiles==23.2.1
```

---

## 四、前端极简架构 (Vue 3 + TypeScript)

### 4.1 项目结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.vue
│   │   ├── DatasetCard.vue
│   │   ├── LoginForm.vue
│   │   └── DatasetDetail.vue
│   ├── views/
│   │   ├── Home.vue
│   │   ├── DatasetList.vue
│   │   ├── Login.vue
│   │   └── Download.vue
│   ├── stores/
│   │   ├── auth.ts       # Pinia store
│   │   └── dataset.ts
│   ├── api/
│   │   ├── auth.ts
│   │   └── dataset.ts
│   └── main.ts
├── vite.config.ts
└── tailwind.config.ts
```

### 4.2 关键页面

**Home.vue - 首页**

* 平台介绍
* 热门数据集展示(前5个下载量最高)
* 快速下载链接

**DatasetList.vue - 数据集列表**

* 搜索和过滤
* 数据集卡片展示
* 分页

**DatasetDetail.vue - 数据集详情**

* 元数据展示
* JSON样本预览
* 下载按钮

**Login.vue - 登录/注册**

* 表单验证
* Token管理

---

## 五、数据存储方案

### 方案A: 本地服务器存储

```python
# 数据集存储在服务器 /data/datasets/ 目录
# 通过Nginx直接提供下载
```

 **优点** : 成本低(仅服务器成本)
 **缺点** : 带宽有限，不支持CDN加速

---

## 六、部署方案 (Docker)

### docker-compose.yml

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      MONGODB_URL: mongodb://root:${MONGO_PASSWORD}@mongodb:27017/dataset_db
      JWT_SECRET_KEY: ${JWT_SECRET}
      OSS_ENDPOINT: ${OSS_ENDPOINT}
      OSS_ACCESS_KEY_ID: ${OSS_ACCESS_KEY_ID}
      OSS_ACCESS_KEY_SECRET: ${OSS_SECRET_KEY}
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

volumes:
  mongo_data:
```

### Nginx配置

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
  
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
  
    # 前端
    location / {
        proxy_pass http://frontend:3000;
    }
  
    # 后端API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 七、阿里云部署步骤

### 7.1 环境准备

1. 购买ECS实例(2核4GB, CentOS 7.x)
2. 购买域名并解析
3. 申请免费SSL证书
4. 安装Docker和docker-compose

### 7.2 一键部署

```bash
# 1. 克隆项目
git clone <your-repo>

# 2. 配置.env文件
cat > .env << EOF
MONGO_PASSWORD=your_secure_password
JWT_SECRET=your_jwt_secret
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
OSS_ACCESS_KEY_ID=your_access_key
OSS_ACCESS_KEY_SECRET=your_secret
EOF

# 3. 启动服务
docker-compose up -d

# 4. 初始化数据库
docker-compose exec backend python -c "from app.database import init_db; init_db()"
```

---

## 八、快速启动清单

* [ ] 本地开发环境搭建
* [ ] 基础认证功能实现
* [ ] 数据集CRUD接口
* [ ] 前端基础页面
* [ ] 文件上传和ZIP生成
* [ ] 下载链接生成
* [ ] 本地测试
* [ ] 购买域名和ECS
* [ ] 配置SSL证书
* [ ] Docker打包部署
* [ ] 线上测试

---

## 九、参考的实验室项目

学习这些项目如何组织数据和元数据:

1. **RoadDamageDetector** (GitHub)
   * 标注格式: Pascal VOC XML
   * 数据组织: 按地区分类
   * 元数据: JSON配置文件
2. **IRRDD** (伊朗实验室)
   * 标注格式: VOC格式
   * 数据集版本控制
   * GitHub Release发布
3. **KITTI数据集** (学术数据集)
   * 完整的元数据描述
   * 详细的使用说明README
   * 分train/val/test集合

---

## 十、成本估算 (年均)

| 项目           | 成本                |
| -------------- | ------------------- |
| ECS 2核4GB     | ~300元/年           |
| 域名(.com)     | ~50元/年            |
| SSL证书        | 免费                |
| OSS存储(100GB) | ~150元/年           |
| 带宽(按需)     | ~200元/年           |
| **总计** | **~700元/年** |

---

## 十一、开发时间估算

| 模块           | 时间                |
| -------------- | ------------------- |
| 后端API        | 2-3周               |
| 前端页面       | 1-2周               |
| 集成测试       | 1周                 |
| 部署上线       | 3-5天               |
| **总计** | **1-1.5个月** |

---

## 十二、后续优化

* 添加用户评论和评分功能
* 数据集版本管理和更新日志
* 生成DOI用于论文引用
* 集成GitHub Actions自动部署
* 添加数据预览功能(图像缩略图)
