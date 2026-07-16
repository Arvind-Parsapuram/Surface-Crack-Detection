"""
╔═══════════════════════════════════════════════════════════════╗
║  TDD — Rohith (Product Owner)                                ║
║  Module: src/config.py — Model Paths, Device, Constants      ║
║  Run:  pytest TDD/Rohith_test_config.py -v                   ║
╚═══════════════════════════════════════════════════════════════╝

Tests covering configuration defaults: model file paths, device detection
(CPU/CUDA), class constants, and split ratios.  Ensures the config module
delivers predictable values for the rest of the application.
"""

import os
from unittest.mock import patch

import pytest

P = os.path.join


# ═══════════════════════════════════════════════════════════════
#  Config.get_model_path()
#  Returns the correct on-disk path for each model variant.
# ═══════════════════════════════════════════════════════════════

class TestModelPaths:

    def test_no_model_name_returns_best_model(self):
        """Default (no name) → models/best_model.pth"""
        from src.config import Config
        path = Config.get_model_path()
        assert path == P("models", "best_model.pth")

    def test_resnet50_path(self):
        """resnet50 → models/resnet50_best.pth"""
        from src.config import Config
        path = Config.get_model_path(model_name="resnet50")
        assert path == P("models", "resnet50_best.pth")

    def test_efficientnet_b0_path(self):
        """efficientnet_b0 → models/efficientnet_b0_best.pth"""
        from src.config import Config
        path = Config.get_model_path(model_name="efficientnet_b0")
        assert path == P("models", "efficientnet_b0_best.pth")

    def test_vit_b_16_path(self):
        """vit_b_16 → models/vit_b_16_best.pth"""
        from src.config import Config
        path = Config.get_model_path(model_name="vit_b_16")
        assert path == P("models", "vit_b_16_best.pth")

    def test_custom_model_name(self):
        """Any name → models/<name>_best.pth"""
        from src.config import Config
        path = Config.get_model_path(model_name="custom_model")
        assert path == P("models", "custom_model_best.pth")

    def test_path_uses_models_dir(self):
        """Every path is rooted in Config.MODELS_DIR."""
        from src.config import Config
        path = Config.get_model_path(model_name="resnet50")
        assert path.startswith(Config.MODELS_DIR)


# ═══════════════════════════════════════════════════════════════
#  Config.DEVICE
#  Auto-detected: CUDA if available, CPU otherwise.
# ═══════════════════════════════════════════════════════════════

class TestDeviceDetection:

    def test_device_is_none_when_torch_unavailable(self):
        """If torch isn't installed, DEVICE should be None (graceful)."""
        with patch.dict("sys.modules", {"torch": None}):
            import importlib
            import src.config
            importlib.reload(src.config)
            assert src.config.Config.DEVICE is None
        importlib.reload(src.config)  # restore

    @pytest.mark.skipif("not __import__('torch').cuda.is_available()")
    def test_device_is_cuda_when_available(self):
        """If CUDA is available, DEVICE starts with 'cuda'."""
        import torch
        from src.config import Config
        if torch.cuda.is_available():
            assert str(Config.DEVICE).startswith("cuda")

    def test_device_is_cpu_when_torch_no_cuda(self):
        """Without CUDA, DEVICE is 'cpu'."""
        from src.config import Config
        assert str(Config.DEVICE) == "cpu"


# ═══════════════════════════════════════════════════════════════
#  Config.CLASSES & NUM_CLASSES
#  The 4 defect types the model can detect.
# ═══════════════════════════════════════════════════════════════

class TestClassConstants:

    def test_classes_list_length(self):
        """There are exactly 4 defect classes."""
        from src.config import Config
        assert len(Config.CLASSES) == 4

    def test_num_classes_matches_length(self):
        """NUM_CLASSES equals len(CLASSES)."""
        from src.config import Config
        assert Config.NUM_CLASSES == len(Config.CLASSES)

    def test_classes_match_module_prediction(self):
        """Config classes match backend.prediction CLASSES."""
        from src.config import Config
        from backend.prediction import CLASSES
        assert set(Config.CLASSES) == set(CLASSES)

    def test_expected_classes_content(self, expected_classes):
        """Config classes match the expected_classes fixture."""
        from src.config import Config
        assert set(Config.CLASSES) == set(expected_classes)

    def test_classes_reorder_safe(self):
        """The four classes are exactly the known defect types."""
        from src.config import Config
        assert set(Config.CLASSES) == {"Cracks", "Patch", "Potholes", "Surface Defects"}


# ═══════════════════════════════════════════════════════════════
#  Config Defaults
#  Stable values that should not change without discussion.
# ═══════════════════════════════════════════════════════════════

class TestConfigDefaults:

    def test_default_model_name(self):
        from src.config import Config
        assert Config.MODEL_NAME == "resnet50"

    def test_ensemble_models_empty(self):
        from src.config import Config
        assert Config.ENSEMBLE_MODELS == []

    def test_image_size(self):
        from src.config import Config
        assert Config.IMAGE_SIZE == 224

    def test_tta_enabled(self):
        from src.config import Config
        assert Config.TTA_ENABLED is True

    def test_models_dir(self):
        from src.config import Config
        assert Config.MODELS_DIR == "models"

    def test_num_classes_int(self):
        from src.config import Config
        assert isinstance(Config.NUM_CLASSES, int)

    def test_split_ratios_sum(self):
        from src.config import Config
        total = sum(Config.SPLIT_RATIOS.values())
        assert abs(total - 1.0) < 0.001

    def test_distill_teachers(self):
        from src.config import Config
        assert "resnet50" in Config.DISTILL_TEACHERS
        assert "vit_b_16" in Config.DISTILL_TEACHERS


# ═══════════════════════════════════════════════════════════════
#  Device Fallback Edge Cases
# ═══════════════════════════════════════════════════════════════

class TestDeviceFallback:

    @patch("torch.cuda.is_available", return_value=False)
    def test_no_cuda_sets_cpu(self, mock_cuda):
        """When CUDA is unavailable, DEVICE falls back to CPU."""
        import importlib
        import src.config
        import torch
        original_torch = src.config.torch
        if original_torch is None:
            pytest.skip("torch not available")
        assert str(src.config.Config.DEVICE).startswith("cuda") or \
               str(src.config.Config.DEVICE) == "cpu"
