
import re

import Events
from Models.Plugins import *
from ..OpenAi.main import Session, OpenAiInteract
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from wcferry import Wcf


@register(
    description="重置当前情景预设[r, reset]",
    version="1.0.0",
    author="For_Lin0601",
    priority=206
)
class ResetCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["reset"] = {
            "is_admin": False,
            "alias": ["r"],
            "summary": "重置当前情景预设",
            "usage": (
                "!reset <预设名|预设编号>"
                " - 用`!default`查看所有预设"
            ),
            "description": (
                "举例: `!reset 提词器`, 或者缩写为`!r 2`(请注意提词器的编号不一定为2)\n"
                "也称之为角色扮演, 或者感觉对话太卡顿可以用`!reset`重置。清除历史记录可能会优化一点对话体验\n"
                "可以自己提供预设给管理员, 让管理员写入`config.py`中的`default_prompt`字段, 即可使用。注意`config.py`中该字段的上下文, 有几个相邻的字段都需要完善。相关提示写在`config.py`中"
            )
        }

    @on(GetQQPersonCommand)
    def cmd_reset(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_reset = r'^r[^a-zA-Z]+'
        if not (re.search(pattern_reset, message) or message == "r" or message.startswith("reset")):
            return
        event.prevent_postorder()
        if message.startswith("reset"):
            message = message[5:].strip()
        else:
            message = message[1:].strip()
        config = self.emit(Events.GetConfig__)
        params = message.split()
        sender_id = kwargs["sender_id"]
        session_name = f"person_{sender_id}"

        reply = ""

        open_ai: OpenAiInteract = self.emit(GetOpenAi__)
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        if len(params) == 0:
            open_ai.sessions_dict[session_name] = Session(
                session_name, "default", config.default_prompt["default"], config.session_expire_time)
            cqhttp.sendPersonMessage(sender_id, config.command_reset_message)
            return

        try:
            import os
            prompts = config.default_prompt
            key_list = list(prompts.keys())
            default_password_path = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "cmdDefault", "default_password.txt")

            # 用文件的方式记录已经输入过密码的人
            with open(default_password_path, 'r') as file:
                account_list = file.readlines()
            account_list = [account.strip()
                            for account in account_list]  # 删除末尾换行符
            permission = True \
                if str(sender_id) in account_list else False  # False表示只能查看部分

            if not permission:
                key_list = [
                    key for key in key_list if key in config.default_prompt_permission]
            if params[0].isdigit() and int(params[0]) <= len(key_list):
                index = int(params[0])-1
                params[0] = key_list[index]
            if not permission and params[0] not in key_list:
                cqhttp.sendPersonMessage(
                    sender_id, "[bot]会话重置失败: 没有找到场景预设: {}".format(params[0]))
                return
            open_ai.sessions_dict[session_name] = Session(
                session_name, params[0], prompts[params[0]], config.session_expire_time)

            reply = config.command_reset_name_message + \
                "{}".format(params[0])
        except Exception as e:
            reply = "[bot]会话重置失败: {}".format(e)

        cqhttp.sendPersonMessage(sender_id, reply)
        return

    @on(GetQQGroupCommand)
    def cmd_reset(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_reset = r'^r[^a-zA-Z]+'
        if not (re.search(pattern_reset, message) or message == "r" or message.startswith("reset")):
            return
        event.prevent_postorder()
        cqhttp = self.emit(Events.GetCQHTTP__)
        cqhttp.sendGroupMessage(kwargs["launcher_id"], "[bot] 群聊暂不支持此命令")

    @on(GetWXCommand)
    def cmd_reset(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        pattern_reset = r'^r[^a-zA-Z]+'
        if not (re.search(pattern_reset, message) or message == "r" or message.startswith("reset")):
            return
        event.prevent_postorder()
        if message.startswith("reset"):
            message = message[5:].strip()
        else:
            message = message[1:].strip()
        config = self.emit(Events.GetConfig__)
        params = message.split()
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        session_name = f"wx_{sender}"

        reply = ""

        open_ai: OpenAiInteract = self.emit(GetOpenAi__)
        wcf: Wcf = self.emit(Events.GetWCF__)
        if len(params) == 0:
            open_ai.sessions_dict[session_name] = Session(
                session_name, "default", config.default_prompt["default"], config.session_expire_time)
            wcf.send_text(config.command_reset_name_message, sender)
            return

        try:
            import os
            prompts = config.default_prompt
            key_list = list(prompts.keys())
            default_password_path = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "cmdDefault", "default_password_wx.txt")

            # 用文件的方式记录已经输入过密码的人
            with open(default_password_path, 'r') as file:
                account_list = file.readlines()
            account_list = [account.strip()
                            for account in account_list]  # 删除末尾换行符
            permission = True if sender in account_list else False  # False表示只能查看部分

            if not permission:
                key_list = [
                    key for key in key_list if key in config.default_prompt_permission]
            if params[0].isdigit() and int(params[0]) <= len(key_list):
                index = int(params[0])-1
                params[0] = key_list[index]
            if not permission and params[0] not in key_list:
                wcf.send_text(
                    "[bot]会话重置失败: 没有找到场景预设: {}".format(params[0]), sender)
                return
            open_ai.sessions_dict[session_name] = Session(
                session_name, params[0], prompts[params[0]], config.session_expire_time)

            reply = config.command_reset_name_message + \
                "{}".format(params[0])
        except Exception as e:
            reply = "[bot]会话重置失败: {}".format(e)

        wcf.send_text(reply, sender)
        return
