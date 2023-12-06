
from typing import Any, Literal, Optional
from pydantic import BaseModel

from ..QQmessage.CQperser import CQParser


class Message:
    pass


class MessageEvent(BaseModel):
    """post_type 为 message 或 message_sent 的上报将会有以下有效通用数据"""

    post_type: str = "message"
    """消息类型"""

    message_type: Literal["private", "group"]
    """私聊 或 群聊"""

    sub_type: Literal[
        "friend", "normal", "anoymous", "group_self", "group", "notice"]
    """消息的子类型"""

    message_id: int
    """消息 ID"""

    user_id: int
    """发送者 QQ 号"""

    message: Any
    """一个消息链"""

    raw_message: str
    """CQ 码格式的消息"""

    font: int = 0
    """字体"""

    sender: object
    """发送者信息, 子类自行实现Sender类"""


class PersonMessageSender(BaseModel):
    """发送者信息(私聊消息内部类)

    尽最大努力提供, 不保证每个字段都一定存在, 也不保证存在的字段都完全正确
    """
    user_id: Optional[int] = None
    """发送者 QQ 号"""

    nickname: Optional[str] = None
    """发送者昵称"""

    sex: Literal["male", "female", "unknown"] = None
    """发送者性别"""

    age: Optional[int] = None
    """发送者年龄"""

    group_id: Optional[int] = None
    """临时群消息来源群号, 否则为 0"""


class PersonMessage(MessageEvent):
    """私聊消息"""

    time: int
    """事件发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    post_type: Literal[
        "message", "message_sent", "request", "notice", "meta_event"]
    """上报类型"""

    target_id: Optional[int] = 0
    """接收者 QQ 号"""

    temp_source: Optional[int] = 0
    """临时会话来源"""

    sender: PersonMessageSender
    """发送者信息"""

    message_type: str = "private"
    """私聊 或 群聊"""

    sub_type: Literal[
        "friend", "group", "group_self", "other"]
    """消息的子类型"""

    def __init__(self, message: str, **kwargs):
        message = CQParser.parseChain(message)
        super().__init__(message=message, **kwargs)


class GroupMessageSender(BaseModel):
    """发送者信息(群聊消息内部类)

    尽最大努力提供, 不保证每个字段都一定存在, 也不保证存在的字段都完全正确
    """
    user_id: int
    """发送者 QQ 号"""

    nickname: str
    """发送者昵称"""

    sex: Literal["male", "female", "unknown"]
    """发送者性别"""

    age: int
    """发送者年龄"""

    card: str
    """群名片/备注"""

    area: str
    """地区"""

    level: str
    """成员等级"""

    role: Literal["owner", "admin", "member"]
    """角色"""

    title: str
    """专属头衔"""


class Anoymous(BaseModel):
    """匿名用户(群聊消息内部类)"""

    id: int
    """匿名用户 ID"""

    name: str
    """匿名用户名称"""

    flag: str
    """匿名用户 flag, 在调用禁言 API 时需要传入"""


class GroupMessage(MessageEvent):
    """群聊消息"""

    time: int
    """事件发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    group_id: int
    """群号"""

    anoymous: Anoymous = None
    """匿名信息, 如果不是匿名消息则为 null"""

    message_type: str = "group"
    """私聊 或 群聊"""

    def __init__(self, message: str, **kwargs):
        message = CQParser.parseChain(message)
        super().__init__(message=message, **kwargs)
