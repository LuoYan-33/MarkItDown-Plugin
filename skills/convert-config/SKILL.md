# /convert-config 命令

配置自动转换功能。

## 用法

```bash
/convert-config enable          # 启用自动转换
/convert-config disable         # 禁用自动转换
/convert-config formats <list>  # 设置需要自动转换的格式
/convert-config status          # 查看当前配置
```

## 功能

- 启用/禁用自动转换
- 配置需要自动转换的格式
- 查看当前配置状态

## 示例

```bash
/convert-config enable
/convert-config formats pdf docx pptx
/convert-config status
```

## 配置说明

- `enabled`：是否启用自动转换（默认：true）
- `formats`：需要自动转换的格式列表（默认：pdf, docx, pptx, xlsx, xls, epub, rtf, html）

## 实现

修改配置文件 `~/.claude/plugins/markitdown-plugin/config.json` 中的自动转换配置。
