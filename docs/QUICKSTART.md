# FusionAI-Lab 快速入门指南

**5 分钟快速启动项目**

---

## 🚀 方式一：Docker 一键启动（推荐）

### 步骤 1: 克隆项目

```bash
git clone https://github.com/FusionAI-Lab/FusionAI-Lab.git
cd FusionAI-Lab
```

### 步骤 2: 启动服务

```bash
docker-compose up -d
```

### 步骤 3: 初始化数据库

```bash
docker-compose exec backend python scripts/seed_data.py
```

### 步骤 4: 访问应用

- **前端**: http://localhost:3000
- **API**: http://localhost:8000
- **Swagger**: http://localhost:8000/docs

### 步骤 5: 测试 API

```bash
# 获取公司列表
curl http://localhost:8000/api/v1/companies/

# 获取融资统计
curl http://localhost:8000/api/v1/funding/stats

# 生成行业报告
curl -X POST http://localhost:8000/api/v1/reports/generate/industry-overview
```

---

## 🛠 方式二：手动启动

### 前置要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 步骤 1: 启动数据库和缓存

```bash
# 使用 Docker 快速启动依赖服务
docker run -d --name postgres \
  -e POSTGRES_DB=fusion_lab \
  -e POSTGRES_USER=fusion_admin \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  postgres:15

docker run -d --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 步骤 2: 配置后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 DATABASE_URL
```

### 步骤 3: 启动后端

```bash
# 数据库迁移（如有）
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 步骤 4: 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

---

## 📊 测试数据

项目包含以下测试数据：

### 公司数据（20 家）

- Commonwealth Fusion Systems (美国)
- Helion Energy (美国)
- TAE Technologies (美国)
- General Fusion (加拿大)
- Tokamak Energy (英国)
- First Light Fusion (英国)
- Marvel Fusion (德国)
- Zap Energy (美国)
- Energy Singularity 能量奇点 (中国)
- StarNet Fusion 星网聚变 (中国)
- 等...

### 融资数据（35+ 条）

- CFS: $1.8B Series B (2021)
- Helion: $500M Series C (2021)
- TAE: $280M Series E (2022)
- General Fusion: $170M Series E (2022)
- 等...

---

## 🔧 常用操作

### 查看日志

```bash
# Docker 方式
docker-compose logs -f backend
docker-compose logs -f frontend

# 手动方式
# 后端日志直接显示在终端
# 前端日志在浏览器控制台
```

### 数据库操作

```bash
# 连接数据库
docker-compose exec postgres psql -U fusion_admin -d fusion_lab

# 查看公司数量
SELECT COUNT(*) FROM companies;

# 查看融资总额
SELECT SUM(amount_usd) FROM funding_rounds;
```

### 重新初始化数据

```bash
# 清空数据库
docker-compose exec postgres psql -U fusion_admin -d fusion_lab -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# 重新填充数据
docker-compose exec backend python scripts/seed_data.py
```

---

## ❓ 常见问题

### Q: 端口被占用怎么办？

A: 修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "3001:3000"  # 前端改为 3001
  - "8001:8000"  # 后端改为 8001
```

### Q: 如何重置数据库？

A: 删除并重建容器：
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend python scripts/seed_data.py
```

### Q: API 返回 404 错误？

A: 检查：
1. 后端服务是否启动
2. 数据库是否初始化
3. API 路径是否正确（/api/v1/...）

### Q: 前端无法连接后端？

A: 检查：
1. 后端是否启动在 8000 端口
2. CORS 配置是否正确
3. 前端 API_BASE_URL 配置

---

## 📚 下一步

启动成功后，你可以：

1. **浏览前端**: 访问 http://localhost:3000 查看可视化界面
2. **测试 API**: 访问 http://localhost:8000/docs 查看 Swagger 文档
3. **生成报告**: 使用报告 API 生成行业分析
4. **查看文档**: 阅读 `docs/技术文档.md` 了解详细信息
5. **贡献代码**: Fork 项目并提交 PR

---

## 🆘 获取帮助

- **GitHub Issues**: https://github.com/FusionAI-Lab/FusionAI-Lab/issues
- **邮箱**: contact@fusionai-lab.com
- **技术文档**: docs/技术文档.md

---

**⚛️ Happy Coding!**
