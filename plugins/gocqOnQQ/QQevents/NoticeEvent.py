
from typing import Literal
from pydantic import BaseModel


class NoticeEvent(BaseModel):
    """post_type 为 notice 的上报会有以下有效通用数据"""

    post_type: str = "notice"
    """消息类型"""

    notice_type: Literal[
        "group_upload",    # 群文件上传
        "group_admin",     # 群管理员变更
        "group_decrease",  # 群成员减少
        "group_increase",  # 群成员增加
        "group_ban",       # 群成员禁言
        "friend_add",      # 好友添加
        "group_recall",    # 群消息撤回
        "friend_recall",   # 好友消息撤回
        "group_card",      # 群名片变更
        "offline_file",    # 离线文件上传
        "client_status",   # 客户端状态变更
        "essence",         # 精华消息
        "notify"           # 系统通知(许多事件无法在手表协议上触发, 皆有声明)
    ]
    """通知类型"""


class PersonMessageRecall(NoticeEvent):
    """好友消息撤回"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    user_id: int
    """好友 QQ 号"""

    message_id: int
    """被撤回的消息 ID"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupMessageRecall(NoticeEvent):
    """群消息撤回"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    group_id: int
    """群号"""

    user_id: int
    """消息发送者 QQ 号"""

    operator_id: int
    """操作者 QQ 号(可能为管理员撤回群友消息导致与 user_id 不同)"""

    message_id: int
    """被撤回的消息 ID"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupIncrease(NoticeEvent):
    """群成员增加"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "approve",  # 管理员已同意入群
        "invite"    # 管理员邀请入群
    ]
    """事件子类型"""

    group_id: int
    """群号"""

    operator_id: int
    """操作者 QQ 号"""

    user_id: int
    """加入者 QQ 号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupDecrease(NoticeEvent):
    """群成员减少"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "leave",   # 主动退群
        "kick",    # 成员被踢
        "kick_me"  # 机器人被踢出
    ]
    """事件子类型"""

    group_id: int
    """群号"""

    operator_id: int
    """操作者 QQ 号(如果是主动退群, 则和 user_id 相同)"""

    user_id: int
    """离开者 QQ 号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupAdmin(NoticeEvent):
    """群管理员变更"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "set",  # 设置管理员
        "unset"  # 取消管理员
    ]
    """事件子类型"""

    group_id: int
    """群号"""

    user_id: int
    """被操作的 QQ 号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupUploadFile(BaseModel):
    """群文件"""

    id: str
    """文件 ID"""

    name: str
    """文件名"""

    size: int
    """文件大小(字节数)"""

    busid: int
    """busid(目前不清楚有什么作用)"""


class GroupUpload(NoticeEvent):
    """群文件上传"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    group_id: int
    """群号"""

    user_id: int
    """上传者 QQ 号"""

    file: GroupUploadFile
    """文件信息"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupBan(NoticeEvent):
    """群禁言"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "ban",      # 禁言
        "lift_ban"  # 解除禁言
    ]
    """事件子类型"""

    group_id: int
    """群号"""

    operator_id: int
    """操作者 QQ 号"""

    user_id: int
    """被禁言的 QQ 号(为全员禁言时为 0)"""

    duration: int
    """禁言时长(秒)(为全员禁言时为-1)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FriendAddEvent(NoticeEvent):
    """好友添加提示"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    user_id: int
    """被添加的 QQ 号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FriendPoke(NoticeEvent):
    """好友戳一戳(双击头像)"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: str = "poke"
    """提示类型"""

    sender_id: int
    """发送者 QQ 号"""

    user_id: int
    """发送者 QQ 号"""

    target_id: int
    """被戳者 QQ 号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupPoke(NoticeEvent):
    """群聊戳一戳(双击头像)[此事件无法在手表协议上触发!!!]"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: str = "poke"
    """提示类型"""

    group_id: int
    """群号"""

    user_id: int
    """发送者 QQ 号"""

    target_id: int
    """被戳者 QQ 号"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LuckyKing(NoticeEvent):
    """群运气王红包提示[此事件无法在手表协议上触发!!!]"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: str = "lucky_king"
    """提示类型"""

    group_id: int
    """群号"""

    user_id: int
    """红包发送者 id"""

    target_id: int
    """运气王 id"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupHonorChange(NoticeEvent):
    """群成员荣誉变更提示[此事件无法在手表协议上触发!!!]"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: str = "honor"
    """提示类型"""

    group_id: int
    """群号"""

    user_id: int
    """成员 QQ 号"""

    honor_type: Literal[
        "talkative",  # 龙王
        "performer",  # 群聊之火
        "emotion"     # 快乐源泉
    ]
    """荣誉变更类型"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupTitleChange(NoticeEvent):
    """群成员头衔变更提示"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: str = "title"
    """提示类型"""

    group_id: int
    """群号"""

    user_id: int
    """变更头衔的用户 QQ 号"""

    title: str
    """获得的新头衔"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupCardChange(NoticeEvent):
    """群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]

    当名片为空, 即 card_new 或者 card_old 为空时, 为空字符串, 不是昵称
    """

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    group_id: int
    """群号"""

    user_id: int
    """成员 QQ 号"""

    card_new: str
    """新名片"""

    card_old: str
    """旧名片"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OfflineFile(BaseModel):
    """离线文件"""

    name: str
    """文件名"""

    size: int
    """文件大小(字节数)"""

    url: str
    """下载链接"""


class OfflineFileupload(NoticeEvent):
    """接收到离线文件"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    user_id: int
    """发送者 QQ 号"""

    file: OfflineFile
    """离线文件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Device(BaseModel):
    """客户端信息, 与API中的类完全一致"""

    app_id: int
    """客户端 ID"""

    device_name: str
    """设备名称"""

    device_kind: str
    """设备类型"""


class ClientStatusChange(NoticeEvent):
    """其他客户端在线状态变更"""

    client: Device
    """客户端信息

    Device 可在 API - 获取当前账号在线客户端列表 查看
    """

    online: bool
    """当前是否在线"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupEssenceChange(NoticeEvent):
    """精华消息变更提示"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "add",    # 添加
        "delete"  # 移出
    ]
    """提示类型"""

    group_id: int
    """群号"""

    sender_id: int
    """消息发送者 QQ 号"""

    operator_id: int
    """操作者 QQ 号"""

    message_id: int
    """消息 ID"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
