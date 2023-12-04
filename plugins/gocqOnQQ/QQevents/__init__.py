
from plugins.gocqOnQQ.QQevents.MessageEvent import (
    PersonMessage, GroupMessage
)
from plugins.gocqOnQQ.QQevents.RequestEvent import (
    FriendAdd, GroupAdd
)
from plugins.gocqOnQQ.QQevents.NoticeEvent import (
    ClientStatusChange,
    PersonMessageRecall, FriendAddEvent,
    FriendPoke, OfflineFileupload,
    GroupMessageRecall, GroupIncrease, GroupDecrease, GroupAdmin, GroupUpload, GroupBan,
    GroupPoke, LuckyKing, GroupHonorChange, GroupTitleChange, GroupCardChange, GroupEssenceChange
)
from plugins.gocqOnQQ.QQevents.MetaEvent import (
    Heartbeat, LifeCycle
)


# from MessageEvent import (
#     PersonMessage, GroupMessage
# )
# from RequestEvent import (
#     FriendAdd, GroupAdd
# )
# from NoticeEvent import (
#     ClientStatusChange,
#     PersonMessageRecall, FriendAddEvent,
#     FriendPoke, OfflineFileupload,
#     GroupMessageRecall, GroupIncrease, GroupDecrease, GroupAdmin, GroupUpload, GroupBan,
#     GroupPoke, LuckyKing, GroupHonorChange, GroupTitleChange, GroupCardChange, GroupEssenceChange
# )
# from MetaEvent import (
#     Heartbeat, LifeCycle
# )


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

    Args:
        json (dict): json

    Returns:
        str: emit事件
        QQevent: 对应的类
    """
    if json["post_type"] not in ws_event_dict:
        return None
    post_type = json["post_type"]
    if post_type in ["message", "message_sent"]:
        return f'QQ_{json["message_type"]}_message', \
            ws_MessageEvent_dict[json["message_type"]](**json)
    elif post_type == "request":
        return f'QQ_{json["request_type"]}_add_event', \
            ws_RequestEvent_dict[json["request_type"]](**json)
    elif post_type == "notice":
        if json["notice_type"] == "notify":
            if json["sub_type"] == "poke":
                if "group_id" in json:
                    return 'QQ_group_poke', \
                        ws_NoticeEvent_dict["notify"]["poke"]["group_poke"](
                            **json)
                return f'QQ_person_poke', \
                    ws_NoticeEvent_dict["notify"]["poke"]["friend_poke"](
                        **json)
            return f'QQ_{json["sub_type"]}', \
                ws_NoticeEvent_dict["notify"][json["sub_type"]](**json)
        return f'QQ_{json["notice_type"]}', \
            ws_NoticeEvent_dict[json["notice_type"]](**json)
    elif post_type == "meta_event":
        return f'QQ_{json["meta_event_type"]}', \
            ws_MetaEvent_dict[json["meta_event_type"]](**json)


# tmp = create_event({
#     "post_type": "meta_event",
#     "meta_event_type": "heartbeat",
#     "time": 123456789,
#     "self_id": 987654321,
#     "status": {
#         "app_initalized": True,
#         "app_enabled": True,
#         "app_good": True,
#         "plugins_good": True,
#         "online": True,
#         "stat": {
#             "packet_received": 12345678,
#             "packet_sent": 12345678,
#             "packet_lost": 12345678,
#             "message_received": 12345678,
#             "message_sent": 12345678,
#             "disconnect_times": 12345678,
#             "lost_times": 12345678,
#             "heartbeat": 12345678,
#             "last_message_time": 12345678,
#         }
#     },
#     "interval": 2345678,
# })
# print(tmp)

# tmp = create_event({
    # "time": 1515204254,
    # "self_id": 10001000,
    # "post_type": "message",
    # "message_type": "private",
    # "sub_type": "friend",
    # "message_id": 12,
    # "user_id": 12345678,
    # "message": 43598,
    # "raw_message": "你好～",
    # "font": 456,
    # "sender": {
        # "nickname": "小不点",
        # "sex": "male",
        # "age": 18
    # }
# }
# )
# print(tmp)
