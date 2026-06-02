# utils/logger.py
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

class Logger:
    """日志工具"""

    def __init__(self, name: str = "markitdown-plugin", log_dir: Optional[str] = None):
        """初始化日志工具"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 设置日志目录
        if log_dir is None:
            home = Path.home()
            log_dir = home / ".claude" / "plugins" / "markitdown-plugin" / "logs"

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 设置日志文件
        log_file = self.log_dir / "plugin.log"

        # 创建 rotating file handler
        # 最大 10MB，保留 5 个文件
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        # 创建 console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加 handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录一般信息"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录警告信息"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """记录错误信息"""
        self.logger.error(message, exc_info=exc_info)

    def get_recent_logs(self, lines: int = 50) -> str:
        """获取最近的日志"""
        log_file = self.log_dir / "plugin.log"
        if not log_file.exists():
            return "暂无日志"

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                return "".join(recent_lines)
        except Exception as e:
            return f"读取日志失败: {e}"

    def clear_logs(self):
        """清除日志"""
        log_file = self.log_dir / "plugin.log"
        if log_file.exists():
            try:
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write("")
                self.info("日志已清除")
            except Exception as e:
                self.error(f"清除日志失败: {e}")

# 全局日志实例
logger = Logger()
