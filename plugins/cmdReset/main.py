
import re

import Events
from Models.Plugins import *
from ..OpenAi.main import Session, OpenAiInteract
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


@register(
    description="重置当前情景预设[r, reset]",
    version="1.0.0",
    author="For_Lin0601",
    priority=206
)
class ResetCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!reset - 重置当前情景预设"
        )

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
        return\
