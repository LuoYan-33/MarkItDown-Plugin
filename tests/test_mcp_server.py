# tests/test_mcp_server.py
import pytest
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from markitdown_mcp.server import MarkItDownMCPServer

def test_mcp_server_init():
    """测试 MCP 服务器初始化"""
    server = MarkItDownMCPServer()
    assert server is not None
