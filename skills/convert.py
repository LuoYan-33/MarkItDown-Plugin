# skills/convert.py
import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from markitdown_mcp.server import MarkItDownMCPServer
from utils.file_detector import FileDetector
from utils.logger import logger

class ConvertSkill:
    """/convert 命令"""

    def __init__(self):
        """初始化"""
        self.server = MarkItDownMCPServer()
        self.file_detector = FileDetector()

    async def execute(self, args: str) -> str:
        """执行命令"""
        try:
            # 解析参数
            file_path = args.strip()

            if not file_path:
                return "用法: /convert <文件路径或URL>"

            logger.info(f"执行 /convert 命令: {file_path}")

            # 判断是 URL 还是本地文件
            if file_path.startswith(("http://", "https://", "data:")):
                # URL
                result = await self.server.mcp.call_tool("convert_to_markdown", {"uri": file_path})
            elif os.path.exists(file_path):
                # 本地文件
                result = await self.server.mcp.call_tool("convert_file_to_markdown", {"file_path": file_path})
            else:
                return f"文件不存在: {file_path}"

            # 提取结果
            if result and len(result) > 0:
                return result[0].text
            else:
                return "转换失败: 未返回结果"

        except Exception as e:
            logger.error(f"执行 /convert 命令失败: {e}")
            return f"执行失败: {str(e)}"

# 命令入口
skill = ConvertSkill()

async def main(args: str) -> str:
    """命令入口函数"""
    return await skill.execute(args)
