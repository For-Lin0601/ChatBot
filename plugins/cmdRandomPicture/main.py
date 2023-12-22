

import time
import re

import Events
from Models.Plugins import *
from .get_picture import process_mod
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from wcferry import Wcf


@register(
    description="随机图片获取[图片]",
    version="1.0.0",
    author="For_Lin0601",
    priority=252
)
class RandomPictureCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["图片"] = {
            "is_admin": False,
            "alias": ["照片", "壁纸", "ranimg", "闪照"],
            "summary": "随机图片获取",
            "usage": "!图片 <番名> <横屏|竖屏>",
            "description": (
                "触发词可选: 照片|图片|壁纸|ranimg|闪照, QQ能发送闪照\n"
                "番名可选, 不定时更新\n"
                "横竖屏可选(实际只区分横屏竖屏, 其余为可识别项): pc|PC|电脑|横屏|pe|PE|android|mobile|手机|安卓|竖屏|random|随机"
            )
        }

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

        start_time = time.time()
        try:
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
        finally:
            stop_time = time.time()
            if stop_time - start_time < 0.5:
                time.sleep(0.5 - (stop_time - start_time))
            cqhttp.recall(tmp_id)

    @on(GetQQGroupCommand)
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
        group_id = kwargs["group_id"]
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)

        logging.debug("发送提示消息: 收到图片获取请求, 网络请求中")
        tmp_id = cqhttp.sendGroupMessage(
            group_id, "[bot] 收到图片获取请求, 网络请求中"
        ).message_id

        start_time = time.time()
        try:
            for _ in range(3):
                try:
                    replay, program = process_mod(params)
                    break
                except:
                    pass
            else:
                replay = "[bot]err: 网络波动, 稍后重试~"

            if isinstance(replay, str):
                cqhttp.sendGroupMessage(group_id, replay)
                return

            replay = replay.toString()

            if re.search('闪照', message):
                try:
                    replay = replay[:-1] + ",type=flash" + replay[-1]
                except:
                    pass
            elif config.include_image_description and program not in [['随机'], ['']]:
                replay = replay + ' '.join(program)

            cqhttp.sendGroupMessage(group_id, replay)
        finally:
            stop_time = time.time()
            if stop_time - start_time < 0.5:
                time.sleep(0.5 - (stop_time - start_time))
            cqhttp.recall(tmp_id)

    @on(GetWXCommand)
    def get_random_picture(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if not (re.search('照片|图片|壁纸|ranimg|闪照', message)
                and not re.search('hi|diray', message)):
            return
        event.prevent_postorder()
        params = re.sub(
            r'^照片|图片|壁纸|ranimg|闪照', '', message
        ).strip().split()
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        wcf: Wcf = self.emit(Events.GetWCF__)

        logging.debug("发送提示消息: 收到图片获取请求, 网络请求中")
        wcf.send_text(
            "[bot] 收到图片获取请求, 网络请求中", sender)
        for _ in range(3):
            try:
                replay, _ = process_mod(params)
                break
            except:
                pass
        else:
            replay = "[bot]err: 网络波动, 稍后重试~"

        if isinstance(replay, str):
            wcf.send_text(sender, replay)
            return

        wcf.send_image(
            os.path.join(os.path.dirname(__file__), "temp.jpg"),
            sender
        )
