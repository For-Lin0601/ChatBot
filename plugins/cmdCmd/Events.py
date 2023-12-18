CmdCmdHelp = "cmd_cmd_help"
"""获取指令用法[!!!此处is_admin仅用作提示, 主线程不对此做额外判断!!!]
```python
    kwargs:
        None

    return:  # 可省略
        dict{
            "**指令名": {
                "is_admin": bool    # 是否为管理员指令, 默认False
                "alias": list       # 别名
                "summary": str      # 概述
                "usage": str        # 用法
                "description": str  # 描述
            }
        }

    示例:  # 以cmd命令为例
        event.return_value["cmd"] = {
            "is_admin": False,  # 为False可省略, 会补充为`用户`
            "alias": [],        # 为[]可省略, 会补充为`无`
            # 以下可省略, 但不建议
            "summary": "显示指令列表",
            "usage": (
                "!cmd\\n"
                " - 显示指令列表\\n"
                "!cmd <指令名>\\n"
                " - 查看指令详情\\n"
                "!cmd all\\n"
                " - 查看所有指令详情"
            ),
            "description": "cmd 可查看到所有指令的详细信息"
        }
```"""
