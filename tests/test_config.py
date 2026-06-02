# tests/test_config.py
import pytest
import json
import os
import tempfile
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.manager import ConfigManager

def test_config_manager_init():
    """测试配置管理器初始化"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        manager = ConfigManager(config_path)
        assert manager.get("ocr.enabled") == False
        assert manager.get("auto_convert.enabled") == True

def test_config_manager_set():
    """测试配置管理器设置值"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        manager = ConfigManager(config_path)
        manager.set("ocr.enabled", True)
        assert manager.get("ocr.enabled") == True

def test_config_manager_save_load():
    """测试配置管理器保存和加载"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        manager = ConfigManager(config_path)
        manager.set("ocr.api_key", "test-key")
        manager.save()

        # 重新加载
        manager2 = ConfigManager(config_path)
        assert manager2.get("ocr.api_key") == "test-key"
