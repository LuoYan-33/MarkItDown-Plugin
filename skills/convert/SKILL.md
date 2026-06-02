# /convert 命令

将文件或 URL 转换为 Markdown 格式。

## 流程

1. **传入** - 用户提供待转换的文件路径或 URL
2. **调用 MCP** - Claude 自动调用 MCP 工具完成转换
3. **返回** - 输出转换后的 Markdown 内容

## 用法

```bash
/convert <文件路径>
/convert <URL>
```

## 示例

```bash
/convert F:/markitdown/项目资产智能管理平台建设方案_试点版_整理后.docx
/convert https://example.com/document.pdf
```

## MCP 工具

- `convert_file_to_markdown` - 转换本地文件
- `convert_to_markdown` - 转换 URL 或文本内容
- `ocr_extract_text` - OCR 提取文本（需启用 OCR）

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

## 注意事项

Claude 会自动调用 MCP 工具，无需手动执行代码。
