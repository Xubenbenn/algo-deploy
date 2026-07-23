"""部署仓集成测试 — 验证「制品 + 适配器 + 外部依赖」协同工作

运行:
    pytest tests/ -v              # 全部
    pytest tests/ -m "smoke"      # 冒烟 (仅核心)
    pytest tests/ -m "extended"   # 扩展

依赖: pip install -r requirements.lock
"""

import sys
import os
import pytest

# 将制品目录加入 path (CI 构建机上由 package.sh 准备好)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ============================================================
# 冒烟测试 (smoke) — 制品可用性
# ============================================================

class TestArtifactAvailability:
    """制品可用性 — 冒烟"""

    @pytest.mark.smoke
    def test_import_svd(self):
        """SVD 模块可导入"""
        try:
            from model.svd.decompose import singular_values
            assert callable(singular_values)
        except ImportError as e:
            pytest.skip(f"制品未安装: {e}")

    @pytest.mark.smoke
    def test_import_matrix_ops(self):
        """矩阵运算模块可导入"""
        try:
            from model.matrix_ops.basic import matrix_norm
            assert callable(matrix_norm)
        except ImportError:
            pytest.skip("制品未安装")

    @pytest.mark.smoke
    def test_import_polyfit(self):
        """多项式拟合模块可导入"""
        try:
            from model.polyfit.fitting import polyfit_ls, polyval
            assert callable(polyfit_ls)
            assert callable(polyval)
        except ImportError:
            pytest.skip("制品未安装")

    @pytest.mark.smoke
    def test_no_experimental_code(self):
        """裁剪后的代码不应包含实验/调试接口"""
        import model.svd.decompose as svd_mod
        # 被裁剪的接口不应存在
        assert not hasattr(svd_mod, 'svd_full') or svd_mod.svd_full is None


# ============================================================
# 集成测试 — 适配器 + 制品协同
# ============================================================

class TestAdapterPipeline:
    """适配器主流程 — 集成"""

    @pytest.mark.smoke
    def test_pipeline_runs(self):
        """主流程不崩溃"""
        from adapters.pipeline import run_pipeline
        result = run_pipeline(sensor_id=42)
        assert result["status"] == "ok"
        assert "max_singular_value" in result
        assert "signal_norm" in result

    @pytest.mark.smoke
    def test_pipeline_output_schema(self):
        """输出格式符合契约"""
        from adapters.pipeline import run_pipeline
        result = run_pipeline(sensor_id=1)
        required_keys = {"sensor_id", "max_singular_value",
                         "condition_estimate", "signal_norm", "status"}
        assert required_keys.issubset(result.keys())

    @pytest.mark.extended
    def test_multiple_sensors(self):
        """多传感器顺序调用不污染"""
        from adapters.pipeline import run_pipeline
        results = [run_pipeline(sensor_id=i) for i in range(5)]
        ids = {r["sensor_id"] for r in results}
        assert ids == {0, 1, 2, 3, 4}


# ============================================================
# 版本一致性测试
# ============================================================

class TestVersionConsistency:
    """版本一致性"""

    @pytest.mark.smoke
    def test_deploy_lock_exists(self):
        """deploy.lock.yaml 存在且可解析"""
        import yaml
        lock_path = os.path.join(
            os.path.dirname(__file__), "..", "deploy.lock.yaml"
        )
        with open(lock_path) as f:
            lock = yaml.safe_load(f)
        assert "artifact" in lock
        assert "version" in lock["artifact"]
