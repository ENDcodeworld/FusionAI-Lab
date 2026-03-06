# Contributing to FusionAI-Lab

感谢你对 FusionAI-Lab 项目的贡献兴趣！

## 如何贡献

### 报告 Bug

1. 在 GitHub Issues 中搜索是否已有相同问题
2. 如果没有，创建新 Issue 并提供：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 环境信息 (OS, Python/Node 版本等)

### 提出新功能

1. 在 GitHub Issues 中讨论你的想法
2. 说明功能用途和实现思路
3. 等待 maintainer 反馈

### 提交代码

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

**Python:**
- 遵循 PEP 8
- 使用 Black 格式化
- 添加类型注解
- 编写单元测试

**TypeScript/JavaScript:**
- 使用 ESLint
- 使用 Prettier 格式化
- 添加类型定义
- 编写测试

### 开发环境设置

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

## 行为准则

- 尊重他人，友好交流
- 对事不对人
- 接受建设性批评
- 帮助新手

## 许可证

提交代码即表示你同意该项目使用 MIT 许可证。

## 联系方式

- Email: contact@fusionai-lab.com
- GitHub Issues: https://github.com/FusionAI-Lab/FusionAI-Lab/issues

---

感谢你的贡献！🎉
