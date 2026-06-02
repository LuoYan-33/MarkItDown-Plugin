# hooks/pre_read.py
import os
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.manager import ConfigManager
from utils.file_detector import FileDetector
from utils.logger import logger

class PreReadHook:
    """pre-read Hook"""

    def __init__(self):
        """初始化"""
        self.config = ConfigManager()
        self.file_detector = FileDetector()

    async def execute(self, file_path: str) -> str:
        """执行 Hook"""
        try:
            logger.info(f"pre-read Hook 执行: {file_path}")

            # 检查自动转换是否启用
            if not self.config.get("auto_convert.enabled", True):
                logger.info("自动转换已禁用，跳过")
                return None

            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.warning(f"文件不存在: {file_path}")
                return None

            # 检查文件是否可转换
            if not self.file_detector.is_convertible(file_path):
                logger.info(f"文件不可转换: {file_path}")
                return None

            # 检查格式是否在自动转换列表中
            file_type = self.file_detector.get_file_type(file_path)
            auto_convert_formats = self.config.get("auto_convert.formats", [])

            if file_type not in auto_convert_formats:
                logger.info(f"文件格式不在自动转换列表中: {file_type}")
                return None

            # 执行转换
            logger.info(f"自动转换文件: {file_path}")

            # 导入 MCP 服务器
            from markitdown_mcp.server import MarkItDownMCPServer
            server = MarkItDownMCPServer()

            # 调用转换工具
            result = await server.mcp.call_tool("convert_file_to_markdown", {"file_path": file_path})

            # 提取结果 - call_tool 返回 (list, list) 元组
            if result and len(result) > 0:
                # 第一个元素是结果列表
                content_list = result[0] if isinstance(result, tuple) else result
                if content_list and len(content_list) > 0:
                    content = content_list[0]
                    if hasattr(content, 'text'):
                        markdown = content.text
                    else:
                        markdown = str(content)
                    logger.info(f"自动转换完成: {file_path}")
                    return markdown
            logger.warning(f"自动转换失败: {file_path}")
            return None

        except Exception as e:
            logger.error(f"pre-read Hook 执行失败: {e}")
            return None

# Hook 入口
if __name__ == "__main__":
    import asyncio

    if len(sys.argv) < 2:
        print("用法: python pre_read.py <文件路径>")
        sys.exit(1)

    file_path = sys.argv[1]
    hook = PreReadHook()
    result = asyncio.run(hook.execute(file_path))

    if result:
        print(result)
