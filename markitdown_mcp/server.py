# markitdown_mcp/server.py
import os
import sys
from pathlib import Path
from typing import Optional

# 添加父目录到路径，以便导入 markitdown
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown
from config.manager import ConfigManager
from utils.file_detector import FileDetector
from utils.logger import logger

class MarkItDownMCPServer:
    """MarkItDown MCP 服务器"""

    def __init__(self):
        """初始化 MCP 服务器"""
        self.config = ConfigManager()
        self.file_detector = FileDetector()
        self.mcp = FastMCP("markitdown")

        # 注册工具
        self._register_tools()

    def _register_tools(self):
        """注册 MCP 工具"""

        @self.mcp.tool()
        async def convert_to_markdown(uri: str) -> str:
            """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
            try:
                logger.info(f"转换 URI: {uri}")

                # 创建 MarkItDown 实例
                md = self._create_markitdown()

                # 转换
                result = md.convert_uri(uri)

                logger.info(f"转换完成: {uri}")
                return result.markdown
            except Exception as e:
                logger.error(f"转换失败: {uri}, 错误: {e}")
                return f"转换失败: {str(e)}"

        @self.mcp.tool()
        async def convert_file_to_markdown(file_path: str) -> str:
            """Convert a local file to markdown"""
            try:
                logger.info(f"转换文件: {file_path}")

                # 检查文件是否存在
                if not os.path.exists(file_path):
                    return f"文件不存在: {file_path}"

                # 检查文件是否可转换
                if not self.file_detector.is_convertible(file_path):
                    return f"不支持的文件格式: {file_path}"

                # 创建 MarkItDown 实例
                md = self._create_markitdown()

                # 转换
                result = md.convert_local(file_path)

                logger.info(f"转换完成: {file_path}")
                return result.markdown
            except Exception as e:
                logger.error(f"转换失败: {file_path}, 错误: {e}")
                return f"转换失败: {str(e)}"

        @self.mcp.tool()
        async def ocr_extract_text(image_path: str) -> str:
            """Extract text from an image using OCR"""
            try:
                logger.info(f"OCR 提取: {image_path}")

                # 检查 OCR 是否启用
                if not self.config.get("ocr.enabled"):
                    return "OCR 功能未启用，请使用 /ocr-config enable 启用"

                # 检查文件是否存在
                if not os.path.exists(image_path):
                    return f"文件不存在: {image_path}"

                # 检查是否为图片
                if not self.file_detector.is_image(image_path):
                    return f"不是图片文件: {image_path}"

                # 创建 MarkItDown 实例（启用 OCR）
                md = self._create_markitdown(enable_ocr=True)

                # 转换
                result = md.convert_local(image_path)

                logger.info(f"OCR 提取完成: {image_path}")
                return result.markdown
            except Exception as e:
                logger.error(f"OCR 提取失败: {image_path}, 错误: {e}")
                return f"OCR 提取失败: {str(e)}"

    def _create_markitdown(self, enable_ocr: bool = False) -> MarkItDown:
        """创建 MarkItDown 实例"""
        # 获取配置
        ocr_enabled = self.config.get("ocr.enabled", False)
        api_key = self.config.get("ocr.api_key", "")
        model = self.config.get("ocr.model", "gpt-4o")
        base_url = self.config.get("ocr.base_url", "")

        # 如果需要 OCR 且配置了 API Key
        if (enable_ocr or ocr_enabled) and api_key:
            try:
                from openai import OpenAI

                # 创建 OpenAI 客户端
                client_kwargs = {"api_key": api_key}
                if base_url:
                    client_kwargs["base_url"] = base_url

                client = OpenAI(**client_kwargs)

                return MarkItDown(
                    enable_plugins=True,
                    llm_client=client,
                    llm_model=model
                )
            except Exception as e:
                logger.warning(f"创建 OCR 客户端失败: {e}，使用普通模式")

        return MarkItDown(enable_plugins=False)

    def run(self, transport: str = "stdio", host: str = "127.0.0.1", port: int = 3001):
        """运行 MCP 服务器"""
        logger.info(f"启动 MCP 服务器: transport={transport}, host={host}, port={port}")

        if transport == "stdio":
            self.mcp.run()
        else:
            # HTTP 模式
            import uvicorn
            from starlette.applications import Starlette
            from mcp.server.sse import SseServerTransport
            from starlette.requests import Request
            from starlette.routing import Mount, Route

            sse = SseServerTransport("/messages/")

            async def handle_sse(request: Request) -> None:
                async with sse.connect_sse(
                    request.scope,
                    request.receive,
                    request._send,
                ) as (read_stream, write_stream):
                    await self.mcp._mcp_server.run(
                        read_stream,
                        write_stream,
                        self.mcp._mcp_server.create_initialization_options(),
                    )

            starlette_app = Starlette(
                debug=True,
                routes=[
                    Route("/sse", endpoint=handle_sse),
                    Mount("/messages/", app=sse.handle_post_message),
                ],
            )

            uvicorn.run(starlette_app, host=host, port=port)


def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Run MarkItDown MCP server")
    parser.add_argument(
        "--http",
        action="store_true",
        help="Run with HTTP transport",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3001,
        help="Port to listen on",
    )

    args = parser.parse_args()

    server = MarkItDownMCPServer()

    if args.http:
        server.run(transport="http", host=args.host, port=args.port)
    else:
        server.run(transport="stdio")


if __name__ == "__main__":
    main()
