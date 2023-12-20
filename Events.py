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
        None

    return:
        config: ModuleType  # 配置模块(以 value = config.key 读取)
```"""

SetConfig__ = "set_config__"
"""设置配置(暂存到 __config.config 中, 不写入 config.py, 热重载后丢失, 请谨慎使用)
```python
    kwargs:
        config: dict  # 配置字典

    return:
        None  # 存在会覆盖
```"""


########## plugin.name='ThreadCtlPlugin' plugin.path='//plugins//__threadctl//main' ##########
SubmitSysTask__ = "submit_sys_task__"
"""提交系统任务
```python
    kwargs:
        fn: callable  # 函数名
        args: list    # 任务参数
        kwargs: dict  # 任务参数

    return:
        Future  # 返回任务
```"""

SubmitAdminTask__ = "submit_admin_task__"
"""提交后台任务
```python
    kwargs:
        fn: callable  # 函数名
        args: list    # 任务参数
        kwargs: dict  # 任务参数

    return:
        Future  # 返回任务
```"""

SubmitUserTask__ = "submit_user_task__"
"""提交用户任务
```python
    kwargs:
        fn: callable  # 函数名
        args: list    # 任务参数
        kwargs: dict  # 任务参数

    return:
        Future  # 返回任务
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


# `QQ_`开头的一律不返回, 插件自行处理并提交下方`post`事件


QQClientSuccess = "QQ_client_success"
"""QQ客户端连接成功(仅在程序启动时触发)(`QQ_`开头一律不用返回)
```python
    kwargs:
        None
```"""


##### 以下是WebSocket事件 #####


##### plugins.gocqOnQQ.QQevents.MessageEvent.py #####
# 普通消息


QQ_private_message = "QQ_private_message"
"""收到QQ消息(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
```"""

QQ_group_message = "QQ_group_message"
"""收到QQ消息(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: GroupMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.RequestEvent.py #####
# 添加请求


QQ_friend_add_event = "QQ_friend_add_event"
"""好友添加请求(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: FriendAdd  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.RequestEvent.py
```"""

QQ_group_add_event = "QQ_group_add_event"
"""群添加请求(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: GroupAdd  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.RequestEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.NoticeEvent.py #####
# 通知


QQ_client_status = "QQ_client_status"
"""其他客户端在线状态变更(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: ClientStatusChange  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_friend_recall = "QQ_friend_recall"
"""好友消息撤回(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: PersonMessageRecall  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""
QQ_friend_add = "QQ_friend_add"
"""好友添加提示
```python
    kwargs:
        QQevents: FriendAddEvent  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_offline_file = "QQ_offline_file"
"""接收到离线文件
```python
    kwargs:
        QQevents: OfflineFileupload  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_recall = "QQ_group_recall"
"""群消息撤回
```python
    kwargs:
        QQevents: GroupMessageRecall  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_increase = "QQ_group_increase"
"""群成员增加
```python
    kwargs:
        QQevents: GroupIncrease  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_decrease = "QQ_group_decrease"
"""群成员减少
```python
    kwargs:
        QQevents: GroupDecrease  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_admin = "QQ_group_admin"
"""群管理员变更
```python
    kwargs:
        QQevents: GroupAdmin  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_upload = "QQ_group_upload"
"""群文件上传
```python
    kwargs:
        QQevents: GroupUpload  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_ban = "QQ_group_ban"
"""群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]

    当名片为空, 即 card_new 或者 card_old 为空时, 为空字符串, 不是昵称
```python
    kwargs:
        QQevents: GroupBan  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_card = "QQ_group_card"
"""群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]
```python
    kwargs:
        QQevents: GroupCardChange  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_essence = "QQ_essence"
"""精华消息变更提示
```python
    kwargs:
        QQevents: GroupEssenceChange  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_lucky_king = "QQ_lucky_king"
"""群运气王红包提示[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        QQevents: LuckyKing  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_honor = "QQ_honor"
"""群成员荣誉变更提示[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        QQevents: GroupHonorChange  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_title = "QQ_title"
"""群成员头衔变更提示
```python
    kwargs:
        QQevents: GroupTitleChange  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_person_poke = "QQ_person_poke"
"""好友戳一戳(双击头像)
```python
    kwargs:
        QQevents: FriendPoke  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_poke = "QQ_group_poke"
"""群聊戳一戳(双击头像)[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        QQevents: GroupPoke  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.MetaEvent.py #####
# 统计信息
# 默认不发送此类信息


QQ_heartbeat = "QQ_heartbeat"
"""心跳包(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: Heartbeat  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MetaEvent.py
```"""

QQ_lifecycle = "QQ_lifecycle"
""" 生命周期(`QQ_`开头一律不用返回)
```python
    kwargs:
        QQevents: Lifecycle  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MetaEvent.py
```"""


########## plugin.name='WeChatbot' plugin.path='//plugins//wcferry//main' ##########
GetWCF__ = "get_wcf__"
"""获取wcf对象
```python
    kwargs:
        None

    return:
        wcf:  # wcf对象, 发送微信消息使用
        # 具体请看 from wcferry import Wcf
```"""


# `WX_`开头的一律不返回, 插件自行处理并提交下方`post`事件


WXClientSuccess = "wx_client_success"
"""微信客户端连接成功(仅在程序启动时触发)(`WX_`开头一律不用返回)
```python
    kwargs:
        None
```"""


##### 微信事件只有WxMsg一种 #####


Wx_msg = "wx_msg"
"""收到微信消息(`WX_`开头一律不用返回)
```python
    kwargs:
        Wx_msg: WxMsg   # 数据存储类
        is_admin: bool  # 是否为管理员
```"""


########## plugin.name='OpenAiInteract' plugin.path='//plugins//OpenAi//main' ##########
GetOpenAi__ = "get_openai__"
"""获取OpenAi对象时触发
```python
    kwargs:
        None

    return:
        openai  # pkg.openai.OpenAI 实例(`return self`)
```"""


########## plugin.name='WxChatTextMessageEventPlugin' plugin.path='//plugins//wcEventTextMessage//main' ##########
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

WXMessageReceived = "qq_person_message_received"
"""收到私聊消息时, 在判断是否应该响应前触发
```python
    kwargs:
        message: WxMsg  # 数据存储类

        return:
        bool:  # 是否阻止默认行为
```"""


########## plugin.name='banWordsUtil' plugin.path='//plugins//banWords//main' ##########
BanWordCheck__ = "ban_word_check__"
"""检查是否包含敏感词
```python
    kwargs:
        message: str  # 消息

    return:
        bool  # 是否包含敏感词
```"""

BanWordProcess__ = "ban_word_process__"
"""处理敏感词
```python
    kwargs:
        message: str  # 消息

    return:
        str  # 处理后的消息
```"""


########## plugin.name='ForwardMessageUtil' plugin.path='//plugins//goForwordMessage//main' ##########

ForwardMessage__ = "forward_message__"
"""包装转发消息, 传入字符串则按一千字左右一分割, 列表则一个元素一分割
```python
    kwargs:
        message: Union[str, list]              # 消息
        qq: Union[int, list] = bot.user_id     # 发送人
        name: Union[str, list] = bot.nickname  # 发送人昵称
        # 若 qq 或 name 为空, 会使用登入号的 QQ号 或 QQ昵称
        # 注意要为列表的话, 三个必须一起为列表, 且长度一致, 将会一一对应转化
        # text列表可为 list[str] , 也可为自定义小列表, 小列表内应为 .plugins.gocqOnQQ.entitiles.components 中的合法QQ消息
        # text内不可混淆两种方式, 在此仅检查text[0]的种类, 不做额外检查

    return:
        Union[list, bool]       # 消息链
```"""


########## plugin.name='TextMessageEventPlugin' plugin.path='//plugins//goEventTextMessage//main' ##########
GetQQPersonCommand = "get_qq_person_command"
"""收到好友命令
```python
    kwargs:
        message: str      # 好友命令文本(去除了前置感叹号)
        message_chain: PersonMessage  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
        launcher_id: int  # 此处与sender_id相等
        sender_id: int    # 发送者ID
        is_admin: bool    # 是否为管理员

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


########## plugin.name='CmdCommand' plugin.path='//plugins//cmdCmd//main' ##########
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



