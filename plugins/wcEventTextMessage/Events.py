GetWXCommand = "get_wx_command"
"""收到微信命令
```python
    kwargs:
        command: str           # 好友命令文本(去除了前置感叹号)
        message: WxMsg         # 数据存储类
        sender: int            # 发送者ID
        roomid: Optional[str]  # (仅群消息有)群 id
        is_admin: bool         # 是否为管理员

    return:
        None
```"""

WXPersonMessageReceived = "wx_message_received"
"""收到私聊消息时, 在判断是否应该响应前触发
```python
    kwargs:
        message: WxMsg  # 数据存储类

        return:
        bool:  # 是否阻止默认行为
```"""
