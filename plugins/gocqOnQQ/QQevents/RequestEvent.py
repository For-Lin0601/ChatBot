
from typing import Literal
from pydantic import BaseModel


class RequestEvent(BaseModel):
    """post_type 为 request 的上报会有以下有效通用数据"""

    post_type: str = "request"
    """消息类型"""

    request_type: str
    """请求类型"""


class FriendAdd(RequestEvent):
    """好友添加请求"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    user_id: int
    """发送请求的 QQ 号"""

    comment: str
    """验证消息"""

    flag: str
    """请求flag, 在调用处理请求的API时需要传入"""

    nickname: str = None
    """自己加的, 方便使用"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupAdd(RequestEvent):
    """群添加请求"""

    time: int
    """事情发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "add",    # 加群请求
        "invite"  # 邀请机器人入群
    ]

    group_id: int
    """群号"""

    user_id: int
    """发送请求的 QQ 号"""

    comment: str
    """验证消息"""

    flag: str
    """请求flag, 在调用处理请求的API时需要传入"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
