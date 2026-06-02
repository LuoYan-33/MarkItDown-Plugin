# /ocr-config 命令

配置 OCR（光学字符识别）功能。

## 用法

```bash
/ocr-config enable          # 启用 OCR
/ocr-config disable         # 禁用 OCR
/ocr-config set-key <API_KEY>  # 设置 API Key
/ocr-config set-model <MODEL>  # 设置模型
/ocr-config set-url <URL>      # 设置 API 基础 URL
/ocr-config status          # 查看当前配置
```

## 功能

- 启用/禁用 OCR 功能
- 配置 LLM API Key
- 配置 LLM 模型
- 配置 API 基础 URL
- 查看当前配置状态

## 示例

```bash
/ocr-config enable
/ocr-config set-key sk-xxxxxxxxxxxx
/ocr-config set-model gpt-4o
/ocr-config status
```

## 配置说明

- `enabled`：是否启用 OCR（true/false）
- `api_key`：LLM API Key（如 OpenAI API Key）
- `model`：LLM 模型名称（如 gpt-4o）
- `base_url`：API 基础 URL（可选，用于兼容其他 API 提供商）

## 实现

修改配置文件 `~/.claude/plugins/markitdown-plugin/config.json` 中的 OCR 配置。
