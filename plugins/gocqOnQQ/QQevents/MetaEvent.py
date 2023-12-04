
from typing import Literal, Union
from pydantic import BaseModel


class MetaEvent(BaseModel):
    """post_type 为 meta_event 的上报会有以下有效数据"""

    post_type: str = "meta_event"
    """消息类型"""

    meta_event_type: str
    """元数据类型"""


class StatusStatistics(BaseModel):
    """统计信息(心跳包内部 的 应用程序状态的 内部类)"""

    packet_received: int
    """收包数"""

    packet_sent: int
    """发包数"""

    packet_lost: int
    """丢包数"""

    message_received: int
    """消息接收数"""

    message_sent: int
    """消息发送数"""

    disconnect_times: int
    """连接断开次数"""

    lost_times: int
    """连接丢失次数"""

    last_message_time: int
    """最后一次消息时间"""


class Status(BaseModel):
    """应用程序状态(心跳包内部类)"""

    app_initialized: bool
    """程序是否初始化完毕"""

    app_enabled: bool
    """程序是否启用"""

    plugins_good: Union[bool, None]
    """插件是否正常运行(可能为null)"""

    app_good: bool
    """程序正常"""

    online: bool
    """是否在线"""

    stat: StatusStatistics
    """统计信息"""


class Heartbeat(MetaEvent):
    """心跳包"""

    time: int
    """事件发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    status: Status
    """应用程序状态"""

    interval: int
    """举例上一次心跳包的时间(毫秒)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LifeCycle(MetaEvent):
    """生命周期"""

    time: int
    """事件发生的时间戳"""

    self_id: int
    """收到事件的机器人 QQ 号"""

    sub_type: Literal[
        "enable",
        "disable",
        "connect"
    ]
    """子类型"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
