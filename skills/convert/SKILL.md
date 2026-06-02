# /convert 命令

将文件或 URL 转换为 Markdown 格式。

## 用法

```bash
/convert <文件路径>
/convert <URL>
```

## 功能

- 支持本地文件转换
- 支持 URL 资源转换
- 支持 markitdown 所有格式

## 示例

```bash
/convert F:/markitdown/项目资产智能管理平台建设方案_试点版_整理后.docx
/convert https://example.com/document.pdf
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

## 实现

调用 MCP 服务器的 `convert_to_markdown` 或 `convert_file_to_markdown` 工具进行转换。
