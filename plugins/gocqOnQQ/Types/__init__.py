from plugins.gocqOnQQ.Types import (
    MessageType,
    RequestType,
    NoticeType,
    MetaEventType
)

post_type_dict = {
    "message": MessageType,
    "message_sent": MessageType,
    "request": RequestType,
    "notice": NoticeType,
    "meta_event": MetaEventType
}
"""消息基类"""
