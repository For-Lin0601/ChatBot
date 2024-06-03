

import Events
from Models.Plugins import *
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


@register(
    description="假借他人之名对话[spoof]",
    version="1.0.0",
    author="For_Lin0601",
    priority=211
)
class SpoofSpeakCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["spoof"] = {
            "is_admin": True,  # 防止别人对虚拟对话引起误解, 只对管理员开放
            "alias": [],
            "summary": "假借他人之名对话",
            "usage": "!spoof",
            "description": (
                "假借他人之名对话\n"
                "有两种获取qq号的方式:\n"
                "一: 第一行是目标qq号, 第二行开始是对话内容, 转发的消息将不拆分, 原样合并成一条消息\n"
                "eg: !spoof 123456\n"
                "独立文本1\n"
                "独立文本2\n"
                "二: 第一行只有`!spoof`, 后续每一段开头是目标qq号, 后面接上对话内容, 模拟群聊的效果, 若开头为`up`, 则表示为本行续接到上行末尾\n"
                "eg: !spoof\n"
                "123456 独立文本1\n"
                "111111 独立文本2\n"
                "up 续接在上一句后面"
            )
        }

    @on(GetQQPersonCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        messages: str = kwargs["message"].strip().split("\n")
        if not messages[0].startswith("spoof"):
            return
        event.prevent_postorder()
        cqHTTP: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        if not kwargs["is_admin"]:
            cqHTTP.sendPersonMessage(kwargs["sender_id"], "[bot] 权限不足")
            return

        if messages[0].strip() != "spoof":
            try:
                qq_number = int(messages[0].replace("spoof", "").strip())
            except:
                cqHTTP.sendPersonMessage(
                    kwargs["sender_id"], "[bot]err: qq号不正确")
                return
            new_message = messages[1:]
            forward_message = self.emit(
                Events.ForwardMessage__,
                message="\n".join(new_message),
                qq=qq_number,
                name="default"
            )

        else:
            qq_number_list = []
            new_message = []
            for i, message in enumerate(messages[1:]):
                qq_number = message.split(" ")[0]
                try:
                    if qq_number == "up":
                        new_message[-1] += "\n" + \
                            " ".join(message.split(" ")[1:])
                    else:
                        qq_number = int(qq_number)
                        qq_number_list.append(qq_number)
                        new_message.append(" ".join(message.split(" ")[1:]))
                except:
                    cqHTTP.sendPersonMessage(
                        kwargs["sender_id"], f"[bot]err: 第{i+1}行qq号[{qq_number}]不正确")
                    return
            forward_message = self.emit(
                Events.ForwardMessage__,
                message=new_message,
                qq=qq_number_list,
                name="default"
            )

        if not forward_message:
            cqHTTP.sendPersonMessage(
                kwargs["sender_id"], f"[bot]err: 消息折叠出错: {new_message}")
            return
        cqHTTP.sendPersonForwardMessage(kwargs["sender_id"], forward_message)
