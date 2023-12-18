
from Models.Plugins import *
from plugins.gocqOnQQ.QQevents.RequestEvent import FriendAdd
from plugins.gocqOnQQ.QQmessage.components import At, Plain

from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


@register(
    description="好友添加处理[add]",
    version="1.0.0",
    author="For_Lin0601",
    priority=208
)
class QQFriendAddPlugin(Plugin):

    def __init__(self):
        self.friend_add_list: list[FriendAdd]
        """待通过好友列表"""

    @on(PluginsLoadingFinished)
    def first_init(self, event: EventContext,  **kwargs):
        self.friend_add_list = []

    @on(PluginsReloadFinished)
    def get_config(self, event: EventContext,  **kwargs):
        self.friend_add_list = self.get_reload_config("friend_add_list")

    def on_reload(self):
        self.set_reload_config("friend_add_list", self.friend_add_list)

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["add"] = {
            "is_admin": True,
            "alias": [],
            "summary": "好友添加处理",
            "usage": "!add [编号]",
            "description": "正数同意, 负数拒绝。最常用的就是`!add 1`或者`!add -1`, 毕竟大多数情况都是从头处理。此处不太稳定, 尽快处理好友申请吧。热重载或者程序重启后不确保好友申请能否留得住, 如果没留住只能上号手动通过了。此外通过`default_password.txt`中的人会自动通过好友申请"
        }

    @on(QQ_friend_add_event)
    def qq_friend_add_event(self, event: EventContext,  **kwargs):
        config = self.emit(GetConfig__)
        friend_add: FriendAdd = kwargs["QQevents"]
        cqhttp: CQHTTP_Protocol = self.emit(GetCQHTTP__)

        # 如果是好友, 忽略
        friend_list = cqhttp.getFriendList()
        for friend in friend_list:
            if friend.user_id == friend_add.user_id:
                return

        event.prevent_postorder()

        # 黑名单直接拒绝
        if friend_add.user_id in config.banned_person_list:
            cqhttp.setFriendRequest(friend_add.flag, False)
            return

        friend_add.nickname = cqhttp.getStrangerInfo(
            friend_add.user_id).nickname

        # # 加入待处理列表
        # # default_password.txt 中的人会直接通过
        default_password_path = os.path.abspath(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'cmdDefault', 'default_password.txt'))
        with open(default_password_path, 'r') as file:
            account_list = file.readlines()
            account_list = [account.strip()
                            for account in account_list]  # 删除末尾换行符

        if str(friend_add.user_id) in account_list:
            cqhttp.setFriendRequest(friend_add.flag)
            cqhttp.NotifyAdmin("检测到 default_password.txt 中存在的好友申请, 已自动通过:\n昵称:{}\nQQ号:{}\n信息:{}".format(
                friend_add.user_id, friend_add.nickname, friend_add.comment))
            import time
            time.sleep(1)
            try:
                cqhttp.sendPersonMessage(
                    friend_add.user_id, f"[bot] 欢迎回来\n\n{config.help_message}")
            except:
                cqhttp.NotifyAdmin(
                    f"warning: 已通过 [{friend_add.nickname}][{friend_add.user_id}] 的好友申请, 但未成功自动执行命令:\n!sent {friend_add.user_id} !help")

        elif friend_add not in self.friend_add_list:
            for i in self.friend_add_list:
                if friend_add.user_id == i.user_id:
                    self.friend_add_list.remove(i)
            self.friend_add_list.append(friend_add)
            cqhttp.NotifyAdmin("新好友请求:\n编号:{}\n昵称:{}\nQQ号:{}\n信息:{}".format(
                len(self.friend_add_list), friend_add.nickname, friend_add.user_id, friend_add.comment))

    @on(GetQQPersonCommand)
    def add_person(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not message.startswith("add"):
            return
        config = self.emit(GetConfig__)
        cqhttp: CQHTTP_Protocol = self.emit(GetCQHTTP__)
        sender_id = kwargs["sender_id"]
        event.prevent_postorder()

        if not kwargs["is_admin"]:
            if kwargs["launcher_id"] == sender_id:  # 私聊
                cqhttp.sendPersonMessage(sender_id, "[bot] 权限不足")
            else:
                cqhttp.sendGroupMessage(
                    kwargs["launcher_id"], [
                        Plain(text="[bot]warning: "),
                        At(qq=sender_id),
                        Plain(text="权限不足")
                    ])
            return
        params = message[3:].split()

        if len(params) == 0:
            if not self.friend_add_list:
                cqhttp.sendPersonMessage(sender_id, "[bot] 暂无好友申请")
                return

            result = "[bot] 以下是尚未通过好友申请的人: "
            for i, req in enumerate(self.friend_add_list):
                result += "\n\n[{}]\n昵称:{}\nQQ号:{}\n信息:{}".format(
                    i + 1, req.nickname, req.user_id, req.comment)
            cqhttp.sendPersonMessage(sender_id, result)
            return

        try:
            index = int(params[0])
        except:
            cqhttp.sendPersonMessage(sender_id, "[bot] 无效的下标")
            return
        if abs(index) > len(self.friend_add_list) or index == 0:
            cqhttp.sendPersonMessage(sender_id, "[bot] 无效的下标")
            return

        req: FriendAdd = self.friend_add_list[abs(index) - 1]
        if index < 0:
            cqhttp.setFriendRequest(req.flag, False)
            self.friend_add_list.remove(req)
            cqhttp.sendPersonMessage(
                sender_id, f"[bot] 已拒绝 [{req.nickname}][{req.user_id}] 的好友申请")
            return

        remark = ' '.join(params[1:]) if len(params) > 1 else None
        cqhttp.setFriendRequest(req.flag, remark=remark)
        import time
        time.sleep(1)
        try:
            cqhttp.sendPersonMessage(
                req.user_id, f"[bot] 已通过你的好友申请\n\n{config.help_message}")
        except:
            cqhttp.sendPersonMessage(
                sender_id, f"warning: 已通过 [{req.nickname}][{req.user_id}] 的好友申请, 但未成功执行发送命令:\n!sent {req.user_id} !help")
        self.friend_add_list.remove(req)
        cqhttp.sendPersonMessage(
            sender_id, "已通过好友申请:\n昵称:{}\nQQ号:{}\n信息:{}\n设置备注(不一定成功):{}".format(
                req.nickname, req.user_id, req.comment, remark if remark else req.nickname))
        return

    @on(GetQQGroupCommand)
    def add_group(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not message.startswith("add"):
            return
        event.prevent_postorder()
        self.emit(GetCQHTTP__).sendGroupMessage(
            group_id=kwargs["launcher_id"], message=f"[bot] 群聊暂不支持此命令"
        )

    @on(GetWXCommand)
    def add_wx(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if not message.startswith("add"):
            return
        event.prevent_postorder()
        self.emit(GetWCF__).send_text(
            "[bot] 微信暂不支持此命令", kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"])
