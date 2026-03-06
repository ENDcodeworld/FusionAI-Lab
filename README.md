# FusionAI-Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)

**核聚变 × AI 数据智能平台**

追踪全球核聚变前沿，提供行业分析、数据可视化和投资咨询服务。

---

## 🎯 项目愿景

成为全球领先的核聚变产业数据智能平台，加速聚变能源商业化进程。

## 📊 核心功能

- **行业数据库**：40+ 聚变公司、融资数据、技术路线
- **智能分析**：AI 驱动的趋势预测和风险评估
- **数据可视化**：交互式聚变实验数据展示
- **研究报告**：深度行业分析和投资洞察
- **科普平台**：聚变技术知识传播

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose

### 后端启动

```bash
# 克隆项目
git clone https://github.com/FusionAI-Lab/FusionAI-Lab.git
cd FusionAI-Lab/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库等

# 数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### Docker 一键启动

```bash
docker-compose up -d
```

访问 http://localhost:3000

## 📁 项目结构

```
FusionAI-Lab/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   └── main.py         # 应用入口
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python 依赖
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── pages/          # 页面
│   │   ├── hooks/          # 自定义 Hooks
│   │   ├── utils/          # 工具函数
│   │   └── App.tsx         # 应用入口
│   ├── public/             # 静态资源
│   └── package.json        # Node 依赖
│
├── data_pipeline/          # 数据处理
│   ├── collectors/         # 数据采集器
│   ├── processors/         # 数据处理器
│   └── pipelines/          # 数据管道
│
├── ai_models/              # AI 模型
│   ├── training/           # 训练脚本
│   ├── models/             # 模型定义
│   └── inference/          # 推理服务
│
├── docs/                   # 项目文档
│   ├── 可行性分析报告.md
│   ├── 技术方案文档.md
│   ├── 变现路径规划.md
│   └── 项目开发计划.md
│
└── docker-compose.yml      # Docker 配置
```

## 🔧 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: PostgreSQL + SQLAlchemy
- **缓存**: Redis
- **消息队列**: Kafka
- **搜索引擎**: Elasticsearch

### 前端
- **框架**: React 18 + TypeScript
- **状态管理**: Zustand
- **UI 组件**: Ant Design
- **可视化**: ECharts + Three.js
- **构建工具**: Vite

### 基础设施
- **容器**: Docker + Kubernetes
- **CI/CD**: GitHub Actions
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack

## 📈 数据源

| 数据类型 | 来源 | 更新频率 |
|----------|------|----------|
| 公司信息 | Crunchbase/官网 | 日更 |
| 融资数据 | PitchBook/公开报道 | 实时 |
| 论文数据 | arXiv/IAEA | 日更 |
| 实验数据 | ITER/JET/EAST | 周更 |
| 新闻资讯 | RSS/社交媒体 | 实时 |

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 开发流程

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📬 联系方式

- **官网**: https://fusionai-lab.com (建设中)
- **邮箱**: contact@fusionai-lab.com
- **微信**: FusionAI-Lab
- **知乎**: @FusionAI-Lab

## 🙏 致谢

感谢以下组织和项目：
- [ITER Organization](https://www.iter.org/)
- [Fusion Industry Association](https://www.fusionindustryassociation.org/)
- [Commonwealth Fusion Systems](https://cfs.energy/)
- [Helion Energy](https://helionenergy.com/)

---

**⚛️ 让聚变能源照亮未来**

*Last Updated: 2026-03-06*
