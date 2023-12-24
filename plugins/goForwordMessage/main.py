
from ..gocqOnQQ.entities.components import Node, Plain

import Events
from .Events import *
from Models.Plugins import *


@register(
    description="QQ长消息转发",
    version="1.0.0",
    author="For_Lin0601",
    priority=1001
)
class ForwardMessageUtil(Plugin):

    @on(ForwardMessage__)
    def check_text(self, event: EventContext, **kwargs) -> list:
        """检查文本是否为长消息, 并转换成该使用的消息链组件"""
        event.prevent_postorder()
        message: str = kwargs["message"]
        if "qq" not in kwargs or "name" not in kwargs:
            cqhttp = self.emit(Events.GetCQHTTP__)
            bot = cqhttp.getLoginInfo()
            qq = kwargs.get("qq", bot.user_id)
            name = kwargs.get("name", bot.nickname)
        else:
            qq = kwargs["qq"]
            name = kwargs["name"]

        if isinstance(name, list) or isinstance(qq, list):
            if len(name) != len(qq) != len(message):
                event.return_value = False
                return

        if isinstance(message, str):
            # 包装转发消息
            segments = []
            while message:
                if len(message) <= 1000:
                    segments.append(message)
                    break
                else:
                    split_index = 1000
                if '\n' in message[split_index:split_index*2]:
                    split_index = message.index(
                        '\n', split_index, split_index*2) + 1
                else:
                    split_index = split_index*2
                segments.append(message[:split_index])
                message = message[split_index:]
        else:
            segments = message

        if not segments:
            event.return_value = False
            return

        if isinstance(qq, list) and isinstance(message[0], str):
            node_list = [Node(
                name=name[i],
                uin=qq[i],
                content=[Plain(text=segment)]
            ) for i, segment in enumerate(segments)]
        elif isinstance(qq, list) and not isinstance(message[0], str):
            node_list = [Node(
                name=name[i],
                uin=qq[i],
                content=segment
            ) for i, segment in enumerate(segments)]
        elif isinstance(message, list) and not isinstance(message[0], str):
            node_list = [Node(
                name=name,
                uin=qq,
                content=segment
            ) for segment in segments]
        else:
            node_list = [Node(
                name=name,
                uin=qq,
                content=[Plain(text=segment)]
            ) for segment in segments]

        event.return_value = node_list
        return
