# skills/convert_config.py
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.manager import ConfigManager
from utils.logger import logger

class ConvertConfigSkill:
    """/convert-config 命令"""

    def __init__(self):
        """初始化"""
        self.config = ConfigManager()

    async def execute(self, args: str) -> str:
        """执行命令"""
        try:
            # 解析参数
            parts = args.strip().split()

            if not parts:
                return self._show_help()

            command = parts[0].lower()

            logger.info(f"执行 /convert-config 命令: {command}")

            if command == "enable":
                return self._enable_auto_convert()
            elif command == "disable":
                return self._disable_auto_convert()
            elif command == "formats":
                if len(parts) < 2:
                    return self._show_formats()
                return self._set_formats(parts[1:])
            elif command == "status":
                return self._show_status()
            else:
                return self._show_help()

        except Exception as e:
            logger.error(f"执行 /convert-config 命令失败: {e}")
            return f"执行失败: {str(e)}"

    def _enable_auto_convert(self) -> str:
        """启用自动转换"""
        self.config.set("auto_convert.enabled", True)
        self.config.save()
        logger.info("自动转换已启用")
        return "✅ 自动转换已启用"

    def _disable_auto_convert(self) -> str:
        """禁用自动转换"""
        self.config.set("auto_convert.enabled", False)
        self.config.save()
        logger.info("自动转换已禁用")
        return "✅ 自动转换已禁用"

    def _set_formats(self, formats: list) -> str:
        """设置格式"""
        self.config.set("auto_convert.formats", formats)
        self.config.save()
        logger.info(f"自动转换格式已设置为: {', '.join(formats)}")
        return f"✅ 自动转换格式已设置为: {', '.join(formats)}"

    def _show_formats(self) -> str:
        """显示当前格式"""
        formats = self.config.get("auto_convert.formats", [])
        return f"当前自动转换格式: {', '.join(formats)}"

    def _show_status(self) -> str:
        """显示状态"""
        enabled = self.config.get("auto_convert.enabled", True)
        formats = self.config.get("auto_convert.formats", [])

        status = f"""自动转换配置状态:
- 启用状态: {'✅ 已启用' if enabled else '❌ 未启用'}
- 支持格式: {', '.join(formats)}"""

        return status

    def _show_help(self) -> str:
        """显示帮助"""
        return """用法: /convert-config <command>

命令:
  enable          启用自动转换
  disable         禁用自动转换
  formats [list]  设置或查看自动转换格式
  status          查看当前配置"""

# 命令入口
skill = ConvertConfigSkill()

async def main(args: str) -> str:
    """命令入口函数"""
    return await skill.execute(args)
