

import Events
from Models.Plugins import *
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


@register(
    description="查看所有情景预设[de, default]",
    version="1.0.0",
    author="For_Lin0601",
    priority=205
)
class DefalutCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!default - 查看所有情景预设"
        )

    @on(GetQQPersonCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not (message.startswith("de ") or message == "de" or
                message.startswith("default")):
            return
        if message.startswith("default"):
            message = message[7:].strip()
        elif message.startswith("de "):
            message = message[2:].strip()
        elif message == "de":
            message = ""
        event.prevent_postorder()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        config = self.emit(Events.GetConfig__)
        sender_id = kwargs["sender_id"]
        params = message.split()

        reply = []
        if len(params) == 0:
            params = [None]
        # 输出目前所有情景预设
        import os
        default_prompt_describe = config.default_prompt_describe
        default_prompt_permission = config.default_prompt_permission
        default_prompt_permission_password = config.default_prompt_permission_password
        prompts = config.default_prompt
        openai = self.emit(Events.GetOpenAi__)
        session_name = openai.sessions_dict.get(f'person_{sender_id}')
        if session_name is None:
            session_name = "default"
        else:
            session_name = session_name.role_name
        reply_str = "[bot] 当前情景预设：{}\n".format(session_name)
        reply_str += "默认情景预设:{}\n\n".format("default")
        reply_str += "用户请使用 !<reset/r> <情景预设名称> 来设置当前情景预设\n\n"
        reply_str += "用户也可使用 !<reset/r> <名称编号> 来设置当前情景预设\n\n"
        reply_str += "\n\n情景预设名称列表:\n"
        default_password_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'default_password.txt')

        # 用文件的方式记录已经输入过密码的人
        with open(default_password_path, 'r') as file:
            account_list = file.readlines()
        account_list = [account.strip() for account in account_list]  # 删除末尾换行符
        permission = True if str(
            sender_id) in account_list else False  # False表示只能查看部分
        if params[0] == default_prompt_permission_password and not str(sender_id) in account_list:
            with open(default_password_path, 'a') as file:
                try:
                    friends_list = cqhttp.getFriendList()
                    for friend in friends_list:
                        if friend.user_id == sender_id:
                            friend_name = friend.remark
                            break
                    cqhttp.sendPersonMessage(
                        sender_id, "[{}][{}]通过default_password验证".format(friend_name, sender_id))
                    cqhttp.NotifyAdmin(
                        "[{}][{}]通过default_password验证".format(friend_name, sender_id))
                    file.write('{}\n'.format(sender_id))
                    permission = True
                except:
                    cqhttp.sendPersonMessage(
                        sender_id, "[bot]err: 意外的错误! 请联系管理员处理!")
            return

        # 查看通过default_password验证的用户
        elif params[0] == "ls":
            if kwargs["is_admin"]:
                account_reply = ""
                friends_list = cqhttp.getFriendList()
                for qq_id in account_list:
                    for friend in friends_list:
                        if friend.user_id == int(qq_id):
                            account_reply += f"\n[{friend.remark}][{qq_id}]"
                            break
                    else:
                        account_reply += f"\n[未知][{qq_id}]"
                cqhttp.sendPersonMessage(
                    sender_id, "通过default_password验证的列表: {}".format(account_reply))
            else:
                cqhttp.sendPersonMessage(sender_id, "[bot] 权限不足")
            return

        # 查看所有情景预设的详细信息
        elif params[0] == "all":
            if kwargs["is_admin"]:
                i = 1
                for key in prompts:
                    reply_str += f"   - [{i}]{key}\n"
                    i += 1
                reply_str += "\n\n详细信息:\n\n"
                i = 1
                segments = []

                # 四个一组, 输出为转发消息
                for key in prompts:
                    reply_str += f"[{i}] 名称: {key}"
                    reply_str += f"\n{prompts[key]}"
                    i += 1
                    segments.append(reply_str)
                    reply_str = ''
                    if (i % 4 == 1 and i != 1) or i == len(prompts)+1:
                        forward = self.emit(
                            Events.ForwardMessage__, message=segments)
                        cqhttp.sendPersonForwardMessage(sender_id, forward)
                        segments = []
            else:
                cqhttp.sendPersonMessage(sender_id, "[bot] 权限不足")
            return

        i = 1
        for key in prompts:
            if key in default_prompt_permission or permission:
                reply_str += "   - [{}]{}\n".format(i, key)
                i += 1
        reply_str += "\n\n详细信息:"
        i = 1
        for key in prompts:
            if key in default_prompt_permission or permission:
                reply_str += "\n\n[{}] 名称: {}".format(i, key)
                i += 1
                if key in default_prompt_describe:
                    reply_str += "\n   - [role] 自我介绍\n   - [content] {}".format(
                        default_prompt_describe[key])
                else:
                    reply_str += "\n   - 该角色尚无自我介绍"

        reply = self.emit(Events.ForwardMessage__, message=reply_str)
        cqhttp.sendPersonForwardMessage(sender_id, reply)
        return
