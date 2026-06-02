# config/manager.py
import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = None):
        """初始化配置管理器"""
        if config_path is None:
            # 默认配置文件路径
            home = Path.home()
            config_path = home / ".claude" / "plugins" / "markitdown-plugin" / "config.json"

        self.config_path = Path(config_path)
        self.config = self._load_default_config()

        # 如果配置文件存在，加载用户配置
        if self.config_path.exists():
            self._load_config()

    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        default_path = Path(__file__).parent / "default.json"
        if default_path.exists():
            with open(default_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_config(self):
        """加载用户配置"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                self._merge_config(self.config, user_config)
        except Exception as e:
            print(f"加载配置文件失败: {e}")

    def _merge_config(self, base: Dict, update: Dict):
        """合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value

    def save(self):
        """保存配置"""
        # 确保目录存在
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def reload(self):
        """重新加载配置"""
        self.config = self._load_default_config()
        if self.config_path.exists():
            self._load_config()
