# skills/convert_log.py
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import logger

class ConvertLogSkill:
    """/convert-log 命令"""

    async def execute(self, args: str) -> str:
        """执行命令"""
        try:
            # 解析参数
            parts = args.strip().split()

            if not parts:
                return self._show_recent_logs()

            command = parts[0].lower()

            logger.info(f"执行 /convert-log 命令: {command}")

            if command == "clear":
                return self._clear_logs()
            elif command == "level":
                if len(parts) < 2:
                    return "用法: /convert-log level <level>"
                return self._set_log_level(parts[1])
            else:
                return self._show_help()

        except Exception as e:
            logger.error(f"执行 /convert-log 命令失败: {e}")
            return f"执行失败: {str(e)}"

    def _show_recent_logs(self, lines: int = 50) -> str:
        """显示最近的日志"""
        logs = logger.get_recent_logs(lines)
        return f"最近 {lines} 条日志:\n\n{logs}"

    def _clear_logs(self) -> str:
        """清除日志"""
        logger.clear_logs()
        return "✅ 日志已清除"

    def _set_log_level(self, level: str) -> str:
        """设置日志级别"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        level = level.upper()

        if level not in valid_levels:
            return f"无效的日志级别: {level}，有效值: {', '.join(valid_levels)}"

        # 设置日志级别
        logger.logger.setLevel(getattr(logger.logger, level))
        logger.info(f"日志级别已设置为: {level}")
        return f"✅ 日志级别已设置为: {level}"

    def _show_help(self) -> str:
        """显示帮助"""
        return """用法: /convert-log <command>

命令:
  (无参数)        查看最近的日志
  clear           清除日志
  level <level>   设置日志级别 (DEBUG, INFO, WARNING, ERROR)"""

# 命令入口
skill = ConvertLogSkill()

async def main(args: str) -> str:
    """命令入口函数"""
    return await skill.execute(args)
