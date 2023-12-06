GetQQPersonCommand = "get_qq_person_command"
"""收到好友命令
```python
    kwargs:
        message: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

    return:
        None
```"""

GetQQGroupCommand = "get_qq_group_command"
"""收到群聊命令
```python
    kwargs:
        message: GroupMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

    return:
        None
```"""

############### 以下为保留选项, TODO ###############

QQPersonMessageReceived = "qq_person_message_received"
"""收到私聊消息时, 在判断是否应该响应前触发
```python
    kwargs:
        message: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

        return:
        bool:  # 是否阻止默认行为
```"""

# QQGroupMessageReceived = "qq_group_message_received"
# """收到群聊消息时, 在判断是否应该响应前触发（所有群消息）

#     kwargs:
#         launcher_type: str 发起对象类型(group/person)
#         launcher_id: int 发起对象ID(群号/QQ号)
#         sender_id: int 发送者ID(QQ号)
#         message_chain: mirai.models.message.MessageChain 消息链
# """

# PersonNormalMessageReceived = "person_normal_message_received"
# """判断为应该处理的私聊普通消息时触发

#     kwargs:
#         launcher_type: str 发起对象类型(group/person)
#         launcher_id: int 发起对象ID(群号/QQ号)
#         sender_id: int 发送者ID(QQ号)
#         text_message: str 消息文本

#     return (optional):
#         alter: str 修改后的消息文本
#         reply: list 回复消息组件列表
# """

# PersonCommandSent = "person_command_sent"
# """判断为应该处理的私聊指令时触发

#     kwargs:
#         launcher_type: str 发起对象类型(group/person)
#         launcher_id: int 发起对象ID(群号/QQ号)
#         sender_id: int 发送者ID(QQ号)
#         command: str 指令
#         params: list[str] 参数列表
#         text_message: str 完整指令文本
#         is_admin: bool 是否为管理员

#     return (optional):
#         alter: str 修改后的完整指令文本
#         reply: list 回复消息组件列表
# """

# GroupNormalMessageReceived = "group_normal_message_received"
# """判断为应该处理的群聊普通消息时触发

#     kwargs:
#         launcher_type: str 发起对象类型(group/person)
#         launcher_id: int 发起对象ID(群号/QQ号)
#         sender_id: int 发送者ID(QQ号)
#         text_message: str 消息文本

#     return (optional):
#         alter: str 修改后的消息文本
#         reply: list 回复消息组件列表
# """

# GroupCommandSent = "group_command_sent"
# """判断为应该处理的群聊指令时触发

#     kwargs:
#         launcher_type: str 发起对象类型(group/person)
#         launcher_id: int 发起对象ID(群号/QQ号)
#         sender_id: int 发送者ID(QQ号)
#         command: str 指令
#         params: list[str] 参数列表
#         text_message: str 完整指令文本
#         is_admin: bool 是否为管理员

#     return (optional):
#         alter: str 修改后的完整指令文本
#         reply: list 回复消息组件列表
# """

# NormalMessageResponded = "normal_message_responded"
# """获取到对普通消息的文字响应时触发

#     kwargs:
#         launcher_type: str 发起对象类型(group/person)
#         launcher_id: int 发起对象ID(群号/QQ号)
#         sender_id: int 发送者ID(QQ号)
#         session: pkg.openai.session.Session 会话对象
#         prefix: str 回复文字消息的前缀
#         response_text: str 响应文本

#     return (optional):
#         prefix: str 修改后的回复文字消息的前缀
#         reply: list 替换回复消息组件列表
# """

# SessionFirstMessageReceived = "session_first_message_received"
# """会话被第一次交互时触发

#     kwargs:
#         session_name: str 会话名称(<launcher_type>_<launcher_id>)
#         session: pkg.openai.session.Session 会话对象
#         default_prompt: str 预设值
# """

# SessionExplicitReset = "session_reset"
# """会话被用户手动重置时触发, 此事件不支持阻止默认行为

#     kwargs:
#         session_name: str 会话名称(<launcher_type>_<launcher_id>)
#         session: pkg.openai.session.Session 会话对象
# """
