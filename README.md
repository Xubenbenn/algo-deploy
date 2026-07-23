# 部署仓 (Deployment Repo)

## 职责

- 胶水适配器代码 (不包含算法逻辑)
- 集成测试 (制品 + 适配器协同验证)
- 打包脚本 (生成机台 .tar.gz 部署包)
- 自动部署流水线

## 目录

```
deployment-repo/
├── adapters/pipeline.py    ← 适配器 (≤50行/文件, 总≤200行)
├── tests/test_integration.py ← 集成测试
├── config/machine.yaml     ← 机台环境参数
├── artifacts/              ← 制品 .tar.gz (CI 自动放置, .gitignore)
├── dist/                   ← 打包产物 (.gitignore)
├── deploy.lock.yaml        ← 版本锁 (CI Bot 更新)
├── requirements.lock       ← 外部依赖锁
├── package.sh              ← 打包脚本
├── ci_deploy.sh            ← CI 自动部署流水线
└── pytest.ini              ← 集成测试配置
```

## 使用

```bash
# 1. 确保制品已构建
(cd ../source-repo && python scripts/build_machine.py -d ../deployment-repo/artifacts/)

# 2. 打包 + 集成测试
bash package.sh

# 3. 自动部署到机台
bash ci_deploy.sh

# 回滚
bash ci_deploy.sh --rollback 1.0.0
```
