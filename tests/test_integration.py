# tests/test_integration.py
import pytest
import asyncio
import os
import tempfile
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入各个模块
from config.manager import ConfigManager
from utils.file_detector import FileDetector
from utils.logger import logger
from markitdown_mcp.server import MarkItDownMCPServer
from skills.convert import ConvertSkill
from skills.ocr_config import OcrConfigSkill
from skills.convert_config import ConvertConfigSkill
from skills.convert_log import ConvertLogSkill
from hooks.pre_read import PreReadHook

def test_config_manager():
    """测试配置管理器"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.json")
        manager = ConfigManager(config_path)

        # 测试默认值
        assert manager.get("ocr.enabled") == False
        assert manager.get("auto_convert.enabled") == True

        # 测试设置值
        manager.set("ocr.enabled", True)
        assert manager.get("ocr.enabled") == True

        # 测试保存和加载
        manager.save()
        manager2 = ConfigManager(config_path)
        assert manager2.get("ocr.enabled") == True

def test_file_detector():
    """测试文件类型检测器"""
    detector = FileDetector()

    # 测试可转换格式
    assert detector.is_convertible("test.pdf") == True
    assert detector.is_convertible("test.docx") == True
    assert detector.is_convertible("test.txt") == False

    # 测试 OCR 支持
    assert detector.is_ocr_supported("test.pdf") == True
    assert detector.is_ocr_supported("test.txt") == False

    # 测试图片检测
    assert detector.is_image("test.png") == True
    assert detector.is_image("test.jpg") == True
    assert detector.is_image("test.txt") == False

def test_mcp_server():
    """测试 MCP 服务器"""
    server = MarkItDownMCPServer()
    assert server is not None

@pytest.mark.asyncio
async def test_convert_skill():
    """测试 /convert 命令"""
    skill = ConvertSkill()
    # 注意：这个测试需要实际的文件
    # 在实际测试中，应该使用测试文件
    pass

@pytest.mark.asyncio
async def test_ocr_config_skill():
    """测试 /ocr-config 命令"""
    skill = OcrConfigSkill()

    # 测试启用 OCR
    result = await skill.execute("enable")
    assert "已启用" in result

    # 测试禁用 OCR
    result = await skill.execute("disable")
    assert "已禁用" in result

    # 测试查看状态
    result = await skill.execute("status")
    assert "OCR 配置状态" in result

@pytest.mark.asyncio
async def test_convert_config_skill():
    """测试 /convert-config 命令"""
    skill = ConvertConfigSkill()

    # 测试启用自动转换
    result = await skill.execute("enable")
    assert "已启用" in result

    # 测试禁用自动转换
    result = await skill.execute("disable")
    assert "已禁用" in result

    # 测试查看状态
    result = await skill.execute("status")
    assert "自动转换配置状态" in result

@pytest.mark.asyncio
async def test_convert_log_skill():
    """测试 /convert-log 命令"""
    skill = ConvertLogSkill()

    # 测试查看日志
    result = await skill.execute("")
    assert "最近" in result

    # 测试清除日志
    result = await skill.execute("clear")
    assert "已清除" in result

@pytest.mark.asyncio
async def test_pre_read_hook():
    """测试 pre-read Hook"""
    hook = PreReadHook()
    # 注意：这个测试需要实际的文件
    # 在实际测试中，应该使用测试文件
    pass
