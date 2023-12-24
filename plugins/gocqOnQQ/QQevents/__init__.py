
from .MessageEvent import (
    PersonMessage, GroupMessage
)
from .RequestEvent import (
    FriendAdd, GroupAdd
)
from .NoticeEvent import (
    ClientStatusChange,
    PersonMessageRecall, FriendAddEvent,
    FriendPoke, OfflineFileupload,
    GroupMessageRecall, GroupIncrease, GroupDecrease, GroupAdmin, GroupUpload, GroupBan,
    GroupPoke, LuckyKing, GroupHonorChange, GroupTitleChange, GroupCardChange, GroupEssenceChange
)
from .MetaEvent import (
    Heartbeat, LifeCycle
)


ws_MessageEvent_dict = {
    "private": PersonMessage,
    "group": GroupMessage,
}

ws_RequestEvent_dict = {
    "friend": FriendAdd,
    "group": GroupAdd,
}

ws_NoticeEvent_dict = {
    "client_status": ClientStatusChange,
    "friend_recall": PersonMessageRecall,
    "friend_add": FriendAddEvent,
    "offline_file": OfflineFileupload,
    "group_recall": GroupMessageRecall,
    "group_increase": GroupIncrease,
    "group_decrease": GroupDecrease,
    "group_admin": GroupAdmin,
    "group_upload": GroupUpload,
    "group_ban": GroupBan,
    "group_card": GroupCardChange,
    "essence": GroupEssenceChange,
    "notify": {
        "lucky_king": LuckyKing,
        "honor": GroupHonorChange,
        "title": GroupTitleChange,
        "poke": {
            "friend_poke": FriendPoke,
            "group_type": GroupPoke,
        },
    },
}

ws_MetaEvent_dict = {
    "heartbeat": Heartbeat,
    "lifecycle": LifeCycle,
}

ws_event_dict = {
    "message": ws_MessageEvent_dict,
    "message_sent": ws_MessageEvent_dict,
    "request": ws_RequestEvent_dict,
    "notice": ws_NoticeEvent_dict,
    "meta_event": ws_MetaEvent_dict,
}


def create_event(json: dict):
    """创造事件
    ```python
    Args:
        json (dict): json

    return:
        str: emit事件
        QQevent: 对应的类
    ```"""
    if json["post_type"] not in ws_event_dict:
        return None

    post_type = json["post_type"]
    if post_type in ["message", "message_sent"]:
        return f'QQ_{json["message_type"]}_message', ws_MessageEvent_dict[json["message_type"]](**json)

    elif post_type == "request":
        return f'QQ_{json["request_type"]}_add_event', ws_RequestEvent_dict[json["request_type"]](**json)

    elif post_type == "notice":
        if json["notice_type"] != "notify":
            return f'QQ_{json["notice_type"]}', ws_NoticeEvent_dict[json["notice_type"]](**json)

        if json["sub_type"] != "poke":
            return f'QQ_{json["sub_type"]}', ws_NoticeEvent_dict["notify"][json["sub_type"]](**json)

        if "group_id" not in json:
            return f'QQ_person_poke', ws_NoticeEvent_dict["notify"]["poke"]["friend_poke"](**json)

        return 'QQ_group_poke', ws_NoticeEvent_dict["notify"]["poke"]["group_poke"](**json)

    elif post_type == "meta_event":
        return f'QQ_{json["meta_event_type"]}', ws_MetaEvent_dict[json["meta_event_type"]](**json)
