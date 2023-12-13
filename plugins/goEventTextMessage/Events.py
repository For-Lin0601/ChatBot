GetQQPersonCommand = "get_qq_person_command"
"""收到好友命令
```python
    kwargs:
        message: str    # 好友命令文本(去除了前置感叹号)
        message_chain: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
        launcher_id: int(此处与sender_id相等)
        sender_id: int  # 发送者ID
        is_admin: bool  # 是否为管理员

    return:
        None
```"""

GetQQGroupCommand = "get_qq_group_command"
"""收到群聊命令
```python
    kwargs:
        message: str      # 群命令文本(去除了前置感叹号)
        message_chain: GroupMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
        launcher_id: int  # 群号
        sender_id: int    # 发送者ID
        is_admin: bool    # 是否为管理员

    return:
        None
```"""

QQPersonMessageReceived = "qq_person_message_received"
"""收到私聊消息时, 在判断是否应该响应前触发
```python
    kwargs:
        message: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

        return:
        bool:  # 是否阻止默认行为
```"""
