# MarkItDown Plugin

Claude Code Plugin，提供文件转换功能，支持 OCR。

## 功能特性

- 支持多种文件格式转换为 Markdown
- 支持 OCR 识别图片中的文字
- 提供 MCP 服务器，供 Claude Code 使用
- 提供 Skills，用于配置和操作
- 提供 Hooks，用于自动检测和转换文件

## 安装

```bash
/plugin install markitdown-plugin
```

## 使用方法

### 手动转换文件

```bash
/convert <文件路径>
/convert <URL>
```

### 配置 OCR

```bash
/ocr-config enable
/ocr-config set-key <API_KEY>
/ocr-config set-model <MODEL>
/ocr-config status
```

### 配置自动转换

```bash
/convert-config enable
/convert-config disable
/convert-config status
```

### 查看日志

```bash
/convert-log
/convert-log clear
```

## 支持的格式

- PDF
- DOCX
- PPTX
- XLSX/XLS
- EPUB
- RTF
- HTML
- CSV, JSON, XML
- 图片 (PNG, JPG, JPEG, GIF, BMP)
- 音频
- Outlook 邮件
- ZIP 文件
- Jupyter Notebook

## 配置文件

配置文件位置：`~/.claude/plugins/markitdown-plugin/config.json`

```json
{
  "ocr": {
    "enabled": false,
    "api_key": "",
    "model": "gpt-4o",
    "base_url": "",
    "prompt": ""
  },
  "auto_convert": {
    "enabled": true,
    "formats": ["pdf", "docx", "pptx", "xlsx", "xls", "epub", "rtf", "html"]
  },
  "mcp": {
    "host": "127.0.0.1",
    "port": 3001
  }
}
```

## 许可证

MIT
