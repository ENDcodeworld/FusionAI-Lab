# FusionAI-Lab ⚛️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)
[![Fusion Industry](https://img.shields.io/badge/Industry-Fusion-orange.svg)](https://www.fusionindustryassociation.org/)
[![GitHub Stars](https://img.shields.io/github/stars/FusionAI-Lab/FusionAI-Lab.svg)](https://github.com/FusionAI-Lab/FusionAI-Lab/stargazers)
[![Issues](https://img.shields.io/github/issues/FusionAI-Lab/FusionAI-Lab.svg)](https://github.com/FusionAI-Lab/FusionAI-Lab/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

<div align="center">

**⚛️ 核聚变 × AI 数据智能平台 | Nuclear Fusion × AI Data Intelligence Platform**

追踪全球核聚变前沿，加速聚变能源商业化进程 — 全面数据库、AI 驱动分析、实时可视化、专业报告

[🚀 快速开始](#-快速开始) · [📚 文档](#-文档) · [✨ 功能特性](#-功能特性) · [🤝 贡献指南](#-贡献指南) · [💬 社区](#-社区)

![FusionAI Demo](./docs/assets/demo.png)
*图：FusionAI-Lab 核聚变融资数据可视化*

</div>

---

## 🌟 项目简介

FusionAI-Lab 是一个专注于核聚变行业的数据智能平台，追踪全球 40+ 核聚变公司、50+ 融资事件，利用 AI 技术提供趋势预测、风险评估和投资洞察，加速聚变能源商业化进程。

### 核心价值

| 痛点 | FusionAI-Lab 解决方案 |
|------|----------------------|
| 📊 行业数据分散 | 全面数据库，持续更新 |
| 🤖 分析门槛高 | AI 驱动趋势预测与洞察 |
| 📈 可视化复杂 | 交互式图表，一目了然 |
| 📑 专业报告昂贵 | 开源报告 + 付费深度分析 |

---

## ✨ 功能特性

### 核心能力

| 功能 | 描述 | 状态 |
|------|------|------|
| **📊 全面数据库** | 收录 40+ 全球核聚变公司，50+ 融资事件，数据持续更新 | ✅ 已完成 |
| **🤖 AI 驱动分析** | 智能趋势预测、风险评估和投资洞察 | 🚧 开发中 |
| **📈 实时可视化** | 交互式融资趋势、技术路线分布和地理分布图 | 🚧 开发中 |
| **📑 专业报告** | 年度概览、季度报告、公司深度分析 | 📋 规划中 |
| **🔬 科普平台** | 核聚变技术知识传播，降低认知门槛 | 📋 规划中 |

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (推荐)

### 一键启动 (Docker)

```bash
# 1. 克隆项目
git clone https://github.com/FusionAI-Lab/FusionAI-Lab.git
cd FusionAI-Lab

# 2. 启动所有服务
docker-compose up -d

# 3. 初始化数据库
docker-compose exec backend python scripts/seed_data.py

# 4. 查看日志
docker-compose logs -f
```

### 手动启动

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

访问地址：
- 🌐 前端：http://localhost:3000
- 📡 API：http://localhost:8000
- 📖 Swagger 文档：http://localhost:8000/docs
- 📖 ReDoc：http://localhost:8000/redoc

---

## 📖 使用示例

### 获取公司数据

```bash
# 获取所有公司
curl http://localhost:8000/api/v1/companies/

# 按技术路线筛选
curl http://localhost:8000/api/v1/companies/?technology_type=Tokamak

# 获取公司详情
curl http://localhost:8000/api/v1/companies/1

# 获取公司融资历史
curl http://localhost:8000/api/v1/companies/1/funding
```

### 获取融资统计

```bash
# 获取融资统计
curl http://localhost:8000/api/v1/funding/stats

# 按技术路线统计
curl http://localhost:8000/api/v1/funding/stats/by-technology

# 按国家统计
curl http://localhost:8000/api/v1/funding/stats/by-country

# 融资时间线
curl http://localhost:8000/api/v1/funding/stats/timeline
```

### 生成报告

```bash
# 生成年度行业概览
curl -X POST http://localhost:8000/api/v1/reports/generate/industry-overview

# 生成公司分析报告
curl -X POST http://localhost:8000/api/v1/reports/generate/company-analysis/1

# 生成季度报告
curl -X POST http://localhost:8000/api/v1/reports/generate/quarterly-report?year=2026&quarter=1
```

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────┐
│                  用户界面层                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   Web    │  │  Mobile  │  │   API    │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
└───────┼─────────────┼─────────────┼─────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│               API Gateway (Nginx)                │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              FastAPI 应用服务                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │  Companies │  │  Funding   │  │  Reports   │ │
│  │    API     │  │    API     │  │    API     │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘ │
└────────┼───────────────┼───────────────┼────────┘
         │               │               │
         ▼               ▼               ▼
┌─────────────────────────────────────────────────┐
│                   数据层                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │PostgreSQL│  │  Redis   │  │  MinIO   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **前端** | React 18 + TypeScript | 现代化 UI 框架 |
| **可视化** | ECharts + Three.js | 2D/3D 数据可视化 |
| **UI 组件** | Ant Design 5 | 企业级组件库 |
| **后端** | FastAPI (Python 3.11) | 高性能异步 API |
| **数据库** | PostgreSQL 15 | 关系型数据库 |
| **缓存** | Redis 7 | 高速缓存 |
| **ORM** | SQLAlchemy (Async) | 异步数据库操作 |
| **部署** | Docker + Compose | 容器化部署 |

---

## 📚 文档

| 文档 | 说明 | 链接 |
|------|------|------|
| 📘 安装指南 | 详细安装步骤 | [查看](docs/installation.md) |
| 📗 快速入门 | 5 分钟上手教程 | [查看](docs/quickstart.md) |
| 📙 API 参考 | 完整 API 文档 | [查看](docs/api.md) |
| 📕 示例代码 | 实用示例集合 | [查看](examples/) |
| 📒 贡献指南 | 如何贡献代码 | [查看](CONTRIBUTING.md) |

---

## 🗺️ 路线图

<div align="center">

| 时间 | 里程碑 | 状态 |
|------|--------|------|
| 2026 Q1 | 数据库建设：公司数据 + 融资事件收录 | ✅ 已完成 |
| 2026 Q2 | 可视化开发：交互式图表 + 地图 | 🚧 进行中 |
| 2026 Q3 | AI 分析：趋势预测 + 风险评估 | 📋 规划中 |
| 2026 Q4 | 报告系统：年度报告 + 深度分析 | 📋 规划中 |

</div>

详细路线图请查看 [ROADMAP.md](docs/ROADMAP.md)

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！

### 如何贡献

1. 🍴 **Fork 仓库** - 创建你自己的 fork
2. 🌿 **创建分支** - `git checkout -b feature/amazing-feature`
3. 💻 **开发** - 编写代码和测试
4. ✅ **测试** - 确保所有测试通过
5. 📤 **提交 PR** - 描述你的改动

### 开发环境设置

```bash
# Fork & Clone
git clone https://github.com/YOUR_USERNAME/FusionAI-Lab.git
cd FusionAI-Lab

# 安装依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 运行测试
pytest tests/ -v
npm run test
```

### 代码规范

- **Python:** 遵循 PEP 8 + Black 格式化
- **TypeScript:** 遵循 ESLint + Prettier
- **提交信息:** 遵循 Conventional Commits 规范

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🧪 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行 API 测试
pytest tests/test_api.py -v
pytest tests/test_models.py -v

# 带覆盖率报告
pytest --cov=app --cov-report=html
```

---

## 📊 项目统计

[![Star History](https://api.star-history.com/svg?repos=FusionAI-Lab/FusionAI-Lab&type=Date)](https://star-history.com/#FusionAI-Lab/FusionAI-Lab&Date)

| 指标 | 数据 |
|------|------|
| ⭐ Stars | 0 |
| 🍴 Forks | 0 |
| 🐛 Issues | 0 |
| 📦 Downloads | 0 |

---

## 💬 社区

### 联系方式

| 平台 | 链接 |
|------|------|
| 🌐 官网 | https://fusionai-lab.com (建设中) |
| 📧 邮箱 | contact@fusionai-lab.com |
| 💬 Discord | [加入社区](https://discord.gg/fusionai) |
| 🐦 Twitter | [@FusionAI_Lab](https://twitter.com/FusionAI_Lab) |
| 📱 微信 | FusionAI-Lab 公众号 |
| 📺 B 站 | @FusionAI-Lab |
| 📖 知乎 | @FusionAI-Lab |

### 加入讨论

- 💬 **Discord 服务器**: [点击加入](https://discord.gg/fusionai)
- 📱 **微信群**: 添加小助手微信 `fusionai_helper` 邀请入群
- 🐦 **Twitter**: [@FusionAI_Lab](https://twitter.com/FusionAI_Lab)

### 相关资源

- [Fusion Industry Association](https://www.fusionindustryassociation.org/)
- [ITER Organization](https://www.iter.org/)
- [Commonwealth Fusion Systems](https://cfs.energy/)
- [Helion Energy](https://helionenergy.com/)

---

## 💰 赞助商

FusionAI-Lab 是开源项目，感谢以下赞助商的支持：

<div align="center">

| 赞助商等级 | 赞助商 | 链接 |
|-----------|--------|------|
| 🏆 **金牌赞助商** | [虚位以待] | [成为赞助商](mailto:sponsor@fusionai-lab.com) |
| 🥈 **银牌赞助商** | [虚位以待] | [成为赞助商](mailto:sponsor@fusionai-lab.com) |
| 🥉 **铜牌赞助商** | [虚位以待] | [成为赞助商](mailto:sponsor@fusionai-lab.com) |

</div>

### 赞助方式

我们接受以下形式的赞助：

- 💰 **资金赞助** - 支持项目持续开发
- 🖥️ **云服务资源** - 服务器、存储、CDN
- 🎯 **推广支持** - 社交媒体分享、技术文章
- 👨‍💻 **人才赞助** - 开发者贡献时间

[👉 立即赞助](https://github.com/sponsors/FusionAI-Lab) | [📧 联系合作](mailto:sponsor@fusionai-lab.com)

---

## 🙏 致谢

感谢以下组织和项目的支持：

- [ITER Organization](https://www.iter.org/)
- [Fusion Industry Association](https://www.fusionindustryassociation.org/)
- [Commonwealth Fusion Systems](https://cfs.energy/)
- [Helion Energy](https://helionenergy.com/)
- [TAE Technologies](https://tae.com/)

---

## 📄 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE) 文件

---

## 👥 团队

- **创始人**: 志哥
- **核心团队**: FusionAI 开发团队
- **贡献者**: [查看贡献者列表](https://github.com/FusionAI-Lab/FusionAI-Lab/graphs/contributors)

---

<div align="center">

### ⭐ 喜欢这个项目吗？

如果这个项目对你有帮助，请给我们一个 **Star** 支持！你的支持是我们持续开发的动力！

[![Star](https://img.shields.io/github/stars/FusionAI-Lab/FusionAI-Lab?style=social)](https://github.com/FusionAI-Lab/FusionAI-Lab)

---

**Made with ❤️ by FusionAI-Lab Team**

⚛️ *让聚变能源照亮未来*

[⬆ 返回顶部](#fusionai-lab-)

</div>

---

## 🔍 SEO 关键词

FusionAI-Lab, 核聚变，聚变能源，AI 数据分析，投资追踪，行业报告，open source, AI, machine learning, nuclear fusion, energy, investment tracking
