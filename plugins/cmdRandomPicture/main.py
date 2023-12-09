

import re

import Events
from Models.Plugins import *
from .get_picture import process_mod
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


@register(
    description="随机图片获取[图片]",
    version="1.0.0",
    author="For_Lin0601",
    priority=252
)
class RandomPictureCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!图片 - 随机图片获取"
        )

    @on(GetQQPersonCommand)
    def get_random_picture(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not (re.search('照片|图片|壁纸|ranimg|闪照', message)
                and not re.search('hi|diray', message)):
            return
        event.prevent_postorder()
        config = self.emit(Events.GetConfig__)
        params = re.sub(
            r'^照片|图片|壁纸|ranimg|闪照', '', message
        ).strip().split()
        sender_id = kwargs["sender_id"]
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)

        logging.debug("发送提示消息: 收到图片获取请求, 网络请求中")
        tmp_id = cqhttp.sendPersonMessage(
            sender_id, "[bot] 收到图片获取请求, 网络请求中"
        ).message_id

        for _ in range(3):
            try:
                replay, program = process_mod(params)
                break
            except:
                pass
        else:
            replay = "[bot]err: 网络波动, 稍后重试~"

        if isinstance(replay, str):
            cqhttp.sendPersonMessage(sender_id, replay)
            cqhttp.recall(tmp_id)
            return

        replay = replay.toString()

        if re.search('闪照', message):
            try:
                replay = replay[:-1] + ",type=flash" + replay[-1]
            except:
                pass
        elif config.include_image_description and program not in [['随机'], ['']]:
            replay = replay + ' '.join(program)

        cqhttp.sendPersonMessage(sender_id, replay)
        cqhttp.recall(tmp_id)
