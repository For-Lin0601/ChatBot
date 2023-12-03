
from ctypes import Union


class Message:
    pass


class MessageType:
    """post_type 为 message 或 message_sent 的上报将会有以下有效通用数据"""

    post_type = "message"
    """消息类型"""

    message_type: Union["private", "group"]
    """私聊 或 群聊"""

    sub_type: Union[
        "friend", "normal", "anoymous", "group_self", "group", "notice"]
    """消息的子类型"""

    message_id: int
    """消息 ID"""

    user_id: int
    """发送者 QQ 号"""

    message: Message
    """一个消息链"""

    raw_message: str
    """CQ 码格式的消息"""

    font: int = 0
    """字体"""

    sender: object
    """发送者信息, 子类自行实现Sender类"""


class Anoymous:
    """匿名用户"""

    id: int
    """匿名用户 ID"""

    name: str
    """匿名用户名称"""

    flag: str
    """匿名用户 flag, 在调用禁言 API 时需要传入"""


class PersonMessage(MessageType):
    """私聊消息"""

    class PersonMessageSender:
        user_id: int
        """发送者 QQ 号"""

        nickname: str
        """发送者昵称"""

        sex: Union["male", "female", "unkown"]
        """发送者性别"""

        age: int
        """发送者年龄"""

        group_id: int = 0
        """临时群消息来源群号, 否则为 0"""

    time: int
    """事件发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    post_type: Union[
        "message", "message_sent", "request", "notice", "meta_event"]
    """上报类型"""

    target_id: int
    """接收者 QQ 号"""

    temp_source: int
    """临时会话来源"""

    sender: PersonMessageSender
    """发送者信息"""

    def __init__(self) -> None:
        self.message_type = "private"
        self.sub_type: Union[
            "friend", "group", "group_self", "other"]


class GroupMessage(MessageType):
    """群聊消息"""

    time: int
    """事件发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    group_id: int
    """群号"""

    anoymous: Anoymous
    """匿名信息, 如果不是匿名消息则为 null"""
