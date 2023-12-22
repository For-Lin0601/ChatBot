

import Events
from .Events import *
from Models.Plugins import *


@register(
    description="显示指令列表[cmd]",
    version="1.0.0",
    author="For_Lin0601",
    priority=201
)
class CmdCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value = {}
        # "is_admin": bool    # 是否为管理员
        # "alias": list       # 别名
        # "summary": str      # 概述
        # "usage": str        # 用法
        # "description": str  # 描述

        event.return_value["cmd"] = {
            "is_admin": False,
            "alias": [],
            "summary": "显示指令列表",
            "usage": (
                "!cmd\n"
                " - 显示指令列表\n"
                "!cmd <指令名>\n"
                " - 查看指令详情\n"
                "!cmd all\n"
                " - 查看所有指令详情"
            ),
            "description": "cmd 可查看到所有指令的详细信息"
        }

    def get_cmd_reply(self, message: str):
        cmd_help = self.emit(CmdCmdHelp)
        for key, value in cmd_help.items():
            if "summary" not in value or not value["summary"]:
                value["summary"] = "暂无描述"
            value["summary"] = f"!{key} - {value['summary']}"
            if "alias" not in value or not value["alias"]:
                value["alias"] = ["无"]
            value["alias"] = ", ".join(value["alias"])
            if "usage" not in value or not value["usage"]:
                value["usage"] = "暂无描述"
            value["usage"] = value["usage"].strip()
            if "description" not in value or not value["description"]:
                value["description"] = "暂无描述"
            if "is_admin" not in value or not value["is_admin"]:
                value["is_admin"] = "用户"
            else:
                value["is_admin"] = "管理员"
        if message == "cmd":
            reply = "[bot] 当前所有指令:\n"
            reply += "- `[]` 为必选参数\n"
            reply += "- `<>` 为选填参数\n"
            reply += "- `!cmd <指令名>`可查看指令详情\n"
            reply += "- `!cmd all`可查看所有指令详情\n\n"
            reply += "\n".join(value["summary"] for value in cmd_help.values())
            return reply

        message = message[3:].strip()
        template = "· 权限: {}\n· 别名: {}\n· 概述: {}\n· 用法:\n{}\n· 描述:\n{}"
        if message == "all":
            reply = "[bot] 当前所有指令详细信息:\n\n"
            reply += "\n\n\n".join([
                ("· 指令: {}\n" + template).format(
                    key,
                    value["is_admin"],
                    value["alias"],
                    value["summary"],
                    value["usage"],
                    value["description"]
                ) for key, value in cmd_help.items()])
            return reply

        if message in cmd_help:
            reply = f"[bot] 指令: {message}\n\n"
            reply += template.format(
                cmd_help[message]["is_admin"],
                cmd_help[message]["alias"],
                cmd_help[message]["summary"],
                cmd_help[message]["usage"],
                cmd_help[message]["description"]
            )
            return reply

        return f"[bot]err: 指令`{message}`不存在或未启用或无描述"

    @on(GetQQPersonCommand)
    def cmd_cmd(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not message.startswith("cmd"):
            return
        event.prevent_postorder()
        reply = self.get_cmd_reply(message)
        self.emit(Events.GetCQHTTP__).sendPersonMessage(
            user_id=kwargs["sender_id"],
            message=reply
        )

    @on(GetQQGroupCommand)
    def cmd_cmd(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not message.startswith("cmd"):
            return
        event.prevent_postorder()
        reply = self.get_cmd_reply(message)
        self.emit(Events.GetCQHTTP__).sendGroupMessage(
            group_id=kwargs["group_id"],
            message=reply
        )

    @on(GetWXCommand)
    def cmd_cmd(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if not message.startswith("cmd"):
            return
        event.prevent_postorder()
        reply = self.get_cmd_reply(message)
        self.emit(Events.GetWCF__).send_text(
            msg=reply,
            receiver=kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        )
