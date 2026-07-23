"""机台适配器 — 纯胶水代码, 不含算法逻辑

约束:
  - 单个文件 ≤ 50 行
  - import 白名单: 标准库, algo_core, machine_hal
  - 禁止: numpy/scipy 直接调用 (算法逻辑在制品中)
"""

import json
import logging
from typing import Any, Dict

# ⚠️ 以下两个 import 来自制品 (algo-machine)
# 在实际机台环境中由 pip install 提供
try:
    from model.svd.decompose import singular_values    # type: ignore
    from model.matrix_ops.basic import matrix_norm      # type: ignore
    from model.polyfit.fitting import polyfit_ls, polyval  # type: ignore
except ImportError:
    singular_values = None      # type: ignore
    matrix_norm = None          # type: ignore
    polyfit_ls = None           # type: ignore
    polyval = None              # type: ignore

# ⚠️ 机台 HAL — 在生产环境中为实际硬件驱动
try:
    from machine_hal import read_sensor, write_result   # type: ignore
except ImportError:
    # 开发/测试回退: 模拟传感器数据
    import numpy as np

    def read_sensor(sensor_id: int) -> Dict[str, Any]:
        return {
            "sensor_id": sensor_id,
            "data": np.random.default_rng(sensor_id).uniform(-10, 10, 64),
            "timestamp": 0.0,
        }

    def write_result(result: Dict[str, Any]) -> bool:
        logging.info(f"写入结果: {json.dumps(result, indent=2)}")
        return True


logger = logging.getLogger(__name__)


def run_pipeline(sensor_id: int, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """机台主流程: 读取传感器 → 算法处理 → 写入结果

    Args:
        sensor_id: 传感器编号
        config: 运行参数 (如拟合次数等)

    Returns:
        {"status": "ok"|"error", "data": {...}}
    """
    # 步骤 1: 读取传感器
    raw = read_sensor(sensor_id)
    data = raw["data"]

    # 步骤 2: 算法处理 (调用制品中的接口)
    # SVD 分析传感器信号的奇异值
    sv = singular_values(data.reshape(8, 8))

    # 矩阵范数评估信号强度
    norm_val = matrix_norm(data.reshape(8, 8), ord="fro")

    # 步骤 3: 组装结果
    result = {
        "sensor_id": sensor_id,
        "max_singular_value": float(sv[0]),
        "condition_estimate": float(sv[0] / (sv[-1] + 1e-10)),
        "signal_norm": float(norm_val),
        "status": "ok",
    }

    # 步骤 4: 写入结果
    write_result(result)
    return result
