#!/bin/bash
# ============================================================
# deploy.sh — 机台端部署脚本
#
# 部署仓双分支模型:
#   main       → 适配器/测试/配置 (人工维护)
#   production → 裁剪后算法源码 (CI 强制推送)
#
# 用法:
#   bash deploy.sh                    # 部署最新 production 源码
#   bash deploy.sh --version v1.0.0   # 指定版本
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

VERSION=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --version) VERSION="$2"; shift ;;
        *) echo "未知参数: $1"; exit 1 ;;
    esac
    shift
done

log() { echo "[$(date +%H:%M:%S)] $*"; }

log "=== 机台部署 ==="

# 1. 拉取 production 分支的裁剪源码
log "拉取 production 分支..."
git fetch origin production

if [ -n "$VERSION" ]; then
    log "  切换到标签: ${VERSION}"
    git checkout "tags/${VERSION}" -- model/ 2>/dev/null || {
        echo "❌ 标签 ${VERSION} 不存在"
        exit 1
    }
else
    git checkout origin/production -- model/
fi

log "  裁剪源码: $(find model/ -name '*.py' | wc -l) 个 .py 文件"

# 2. 安装依赖
log "安装依赖..."
pip install -r requirements.lock --quiet 2>&1 | tail -1

# 3. 冒烟测试
log "冒烟测试..."
python3 -c "
import sys; sys.path.insert(0, '.')
from model.svd.decompose import singular_values
import numpy as np
sv = singular_values(np.eye(3))
assert len(sv) == 3, f'SVD 失败: {sv}'
print(f'  ✅ SVD ok, 奇异值: {sv}')
print(f'  ✅ 部署就绪')
"

log ""
log "============================================"
log "✅ 部署完成"
log "   源码: model/ ($(du -sh model/ | cut -f1))"
log "============================================"
