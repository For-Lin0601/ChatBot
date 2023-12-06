########## 主线程必选项 ##########

PluginsLoadingFinished = "plugins_loading_finished"
"""插件首次加载时触发(程序启动时)

    kwargs:
        None

    return:
        None
"""

PluginsReloadFinished = "plugins_reload_finished"
"""插件重载完成时触发, 等同于在`plugin.__init__`中判断`not self.is_first_init()`后的代码块

    kwargs:
        None

    return:
        None
"""

# 若希望程序启动和重载完后都触发, 可以使用
# @on(PluginsLoadingFinished)
# @on(PluginsReloadFinished)
# def your_function(self, event: EventContext, **kwargs):
#   ...



########## plugin.name='Log' plugin.path='//plugins//__log//main' ##########
SetLogs__ = "set_logs__"
"""设置日志(在有插件修改了日志之后)
```python
    kwargs:
        None

    return:
        None
```"""


########## plugin.name='Config' plugin.path='//plugins//__config//main' ##########
GetConfig__ = "get_config__"
"""获取配置
```python
    kwargs:
        config_name: str 配置名称(为空则返回配置字典)

    return:
        config: ModuleType 配置模块(以 value = config.key 读取)
```"""

SetConfig__ = "set_config__"
"""设置配置(暂存到 __config.config 中, 不写入 config.py)
```python
    kwargs:
        config: dict 配置字典
```"""



########## plugin.name='ThreadCtlPlugin' plugin.path='//plugins//__threadctl//main' ##########
SubmitSysTask__ = "submit_sys_task__"
"""提交系统任务
```python
    kwargs:
        fn: 任务
        args: 任务参数
        kwargs: 任务参数

    return:
        Future: 返回任务
```"""

SubmitAdminTask__ = "submit_admin_task__"
"""提交后台任务
```python
    kwargs:
        fn: 任务
        args: 任务参数
        kwargs: 任务参数

    return:
        Future: 返回任务
```"""

SubmitUserTask__ = "submit_user_task__"
"""提交用户任务
```python
    kwargs:
        fn: 任务
        args: 任务参数
        kwargs: 任务参数

    return:
        Future: 返回任务
```"""



########## plugin.name='QQbot' plugin.path='//plugins//gocqOnQQ//main' ##########
GetCQHTTP__ = "get_cqhttp__"
"""获取CQHTTP对象
```python
    kwargs:
        None

    return:
        CQHTTP_pretocol: CQHTTP对象, 发送QQ消息使用, 具体请看 plugins.gocqOnQQ.CQHTTP_pretocol
```"""

QQClientSuccess = "QQ_client_success"
"""QQ客户端连接成功(仅在程序启动时触发)(`QQ_`开头一律不用返回)
```python
    kwargs:
        None
```"""


# `QQ_`开头的一律不返回, 插件自行处理并提交下方`post`事件


##### 以下是WebSocket事件 #####


##### plugins.gocqOnQQ.QQevents.MessageEvent.py #####
# 普通消息


QQ_private_message = "QQ_private_message"
"""收到QQ消息(`QQ_`开头一律不用返回)
```python
    kwargs:
        PersonMessage:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
```"""

QQ_group_message = "QQ_group_message"
"""收到QQ消息(`QQ_`开头一律不用返回)
```python
    kwargs:
        GroupMessage:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.RequestEvent.py #####
# 添加请求


QQ_friend_add_event = "QQ_friend_add_event"
"""好友添加请求(`QQ_`开头一律不用返回)
```python
    kwargs:
        FriendAdd:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.RequestEvent.py
```"""

QQ_group_add_event = "QQ_group_add_event"
"""群添加请求(`QQ_`开头一律不用返回)
```python
    kwargs:
        GroupAdd:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.RequestEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.NoticeEvent.py #####
# 通知


QQ_client_status = "QQ_client_status"
"""其他客户端在线状态变更(`QQ_`开头一律不用返回)
```python
    kwargs:
        ClientStatusChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_friend_recall = "QQ_friend_recall"
"""好友消息撤回(`QQ_`开头一律不用返回)
```python
    kwargs:
        PersonMessageRecall:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""
QQ_friend_add = "QQ_friend_add"
"""好友添加提示
```python
    kwargs:
        FriendAddEvent:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_offline_file = "QQ_offline_file"
"""接收到离线文件
```python
    kwargs:
        OfflineFileupload:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_recall = "QQ_group_recall"
"""群消息撤回
```python
    kwargs:
        GroupMessageRecall:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_increase = "QQ_group_increase"
"""群成员增加
```python
    kwargs:
        GroupIncrease:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_decrease = "QQ_group_decrease"
"""群成员减少
```python
    kwargs:
        GroupDecrease:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_admin = "QQ_group_admin"
"""群管理员变更
```python
    kwargs:
        GroupAdmin:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_upload = "QQ_group_upload"
"""群文件上传
```python
    kwargs:
        GroupUpload:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_ban = "QQ_group_ban"
"""群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]

    当名片为空, 即 card_new 或者 card_old 为空时, 为空字符串, 不是昵称
```python
    kwargs:
        GroupBan:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_card = "QQ_group_card"
"""群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]
```python
    kwargs:
        GroupCardChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_essence = "QQ_essence"
"""精华消息变更提示
```python
    kwargs:
        GroupEssenceChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_lucky_king = "QQ_lucky_king"
"""群运气王红包提示[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        LuckyKing:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_honor = "QQ_honor"
"""群成员荣誉变更提示[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        GroupHonorChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_title = "QQ_title"
"""群成员头衔变更提示
```python
    kwargs:
        GroupTitleChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_person_poke = "QQ_person_poke"
"""好友戳一戳(双击头像)
```python
    kwargs:
        FriendPoke:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_poke = "QQ_group_poke"
"""群聊戳一戳(双击头像)[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        GroupPoke:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.MetaEvent.py #####
# 统计信息
# 默认不发送此类信息


QQ_heartbeat = "QQ_heartbeat"
"""心跳包(`QQ_`开头一律不用返回)
```python
    kwargs:
        Heartbeat:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MetaEvent.py
```"""

QQ_lifecycle = "QQ_lifecycle"
""" 生命周期(`QQ_`开头一律不用返回)
```python
    kwargs:
        Lifecycle:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MetaEvent.py
```"""



########## plugin.name='OpenAIInteract' plugin.path='//plugins//OpenAi//main' ##########
GetOpenAi__ = "get_openai__"
"""获取OpenAi对象时触发
```python
    kwargs:
        None

    return:
        openai: pkg.openai.OpenAI
```"""

SessionExpired = "session_expired"
"""会话过期时触发
```python
    kwargs:
        session_name: str 会话名称(<launcher_type>_<launcher_id>)
        session: pkg.openai.session.Session 会话对象
        session_expire_time: int 已设置的会话过期时间(秒)
```"""

KeyExceeded = "key_exceeded"
"""api-key超额时触发
```python
    kwargs:
        key_name: str 超额的api-key名称
        usage: dict 超额的api-key使用情况
        exceeded_keys: list[str] 超额的api-key列表
```"""

KeySwitched = "key_switched"
"""api-key超额切换成功时触发, 此事件不支持阻止默认行为
```python
    kwargs:
        key_name: str 切换成功的api-key名称
        key_list: list[str] api-key列表
```"""



########## plugin.name='TextMessagePlugin' plugin.path='//plugins//goTextMessage//main' ##########
GetQQPersonCommand = "get_person_command"
"""收到好友命令
```python
    kwargs:
        message: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

    return:
        None
```"""

GetGroupCommand = "get_group_command"
"""收到群聊命令
```python
    kwargs:
        message: GroupMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

    return:
        None
```"""

############### 以下为保留选项, TODO ###############

PersonMessageReceived = "person_message_received"
"""收到私聊消息时, 在判断是否应该响应前触发
```python
    kwargs:
        message: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py

        return:
        bool:  # 是否阻止默认行为
```"""

# GroupMessageReceived = "group_message_received"
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



########## plugin.name='banWordsUtil' plugin.path='//plugins//banWords//main' ##########
BanWordCheck__ = "ban_word_check__"
"""检查是否包含敏感词
```python
    kwargs:
        message: str 消息

    return:
        bool 是否包含敏感词
```"""

BanWordProcess__ = "ban_word_process__"
"""处理敏感词
```python
    kwargs:
        message: str 消息

    return:
        str 处理后的消息
```"""
