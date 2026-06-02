# /convert-log 命令

查看和管理日志。

## 用法

```bash
/convert-log              # 查看最近的日志
/convert-log clear        # 清除日志
/convert-log level <level>  # 设置日志级别
```

## 功能

- 查看最近的日志
- 清除日志
- 设置日志级别

## 示例

```bash
/convert-log
/convert-log clear
/convert-log level DEBUG
```

## 日志级别

- `DEBUG`：详细的调试信息
- `INFO`：一般信息（如转换开始、完成）
- `WARNING`：警告信息（如 OCR 失败，降级处理）
- `ERROR`：错误信息（如转换失败、配置错误）

## 日志文件位置

`~/.claude/plugins/markitdown-plugin/logs/plugin.log`

## 实现

读取和管理日志文件 `~/.claude/plugins/markitdown-plugin/logs/plugin.log`。
