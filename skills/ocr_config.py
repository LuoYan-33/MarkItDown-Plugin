# skills/ocr_config.py
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.manager import ConfigManager
from utils.logger import logger

class OcrConfigSkill:
    """/ocr-config 命令"""

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

            logger.info(f"执行 /ocr-config 命令: {command}")

            if command == "enable":
                return self._enable_ocr()
            elif command == "disable":
                return self._disable_ocr()
            elif command == "set-key":
                if len(parts) < 2:
                    return "用法: /ocr-config set-key <API_KEY>"
                return self._set_api_key(parts[1])
            elif command == "set-model":
                if len(parts) < 2:
                    return "用法: /ocr-config set-model <MODEL>"
                return self._set_model(parts[1])
            elif command == "set-url":
                if len(parts) < 2:
                    return "用法: /ocr-config set-url <URL>"
                return self._set_base_url(parts[1])
            elif command == "status":
                return self._show_status()
            else:
                return self._show_help()

        except Exception as e:
            logger.error(f"执行 /ocr-config 命令失败: {e}")
            return f"执行失败: {str(e)}"

    def _enable_ocr(self) -> str:
        """启用 OCR"""
        self.config.set("ocr.enabled", True)
        self.config.save()
        logger.info("OCR 已启用")
        return "✅ OCR 已启用"

    def _disable_ocr(self) -> str:
        """禁用 OCR"""
        self.config.set("ocr.enabled", False)
        self.config.save()
        logger.info("OCR 已禁用")
        return "✅ OCR 已禁用"

    def _set_api_key(self, api_key: str) -> str:
        """设置 API Key"""
        self.config.set("ocr.api_key", api_key)
        self.config.save()
        logger.info("API Key 已设置")
        return "✅ API Key 已设置"

    def _set_model(self, model: str) -> str:
        """设置模型"""
        self.config.set("ocr.model", model)
        self.config.save()
        logger.info(f"模型已设置为: {model}")
        return f"✅ 模型已设置为: {model}"

    def _set_base_url(self, base_url: str) -> str:
        """设置 API 基础 URL"""
        self.config.set("ocr.base_url", base_url)
        self.config.save()
        logger.info(f"API 基础 URL 已设置为: {base_url}")
        return f"✅ API 基础 URL 已设置为: {base_url}"

    def _show_status(self) -> str:
        """显示状态"""
        enabled = self.config.get("ocr.enabled", False)
        api_key = self.config.get("ocr.api_key", "")
        model = self.config.get("ocr.model", "gpt-4o")
        base_url = self.config.get("ocr.base_url", "")

        status = f"""OCR 配置状态:
- 启用状态: {'✅ 已启用' if enabled else '❌ 未启用'}
- API Key: {'✅ 已设置' if api_key else '❌ 未设置'}
- 模型: {model}
- API 基础 URL: {base_url or '未设置'}"""

        return status

    def _show_help(self) -> str:
        """显示帮助"""
        return """用法: /ocr-config <command>

命令:
  enable          启用 OCR
  disable         禁用 OCR
  set-key <key>   设置 API Key
  set-model <m>   设置模型
  set-url <url>   设置 API 基础 URL
  status          查看当前配置"""

# 命令入口
skill = OcrConfigSkill()

async def main(args: str) -> str:
    """命令入口函数"""
    return await skill.execute(args)
