

import io
import json

import requests
import Events
from PIL import Image

from .add_text_to_image import add_text_to_image as add_text_to_image
from Models.Plugins import *
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from ..gocqOnQQ.QQevents.MessageEvent import PersonMessage
from wcferry import Wcf, WxMsg


@register(
    description="添加水印[水印]",
    version="1.0.0",
    author="For_Lin0601",
    priority=251
)
class WaterMarkCommand(Plugin):

    def __init__(self):
        self.qq_watermark_json_file_path = os.path.join(
            os.path.dirname(__file__), "watermark.json")
        if not os.path.exists(self.qq_watermark_json_file_path):
            with open(self.qq_watermark_json_file_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

        self.wx_watermark_json_file_path = os.path.join(
            os.path.dirname(__file__), "watermark_wx.json")
        if not os.path.exists(self.wx_watermark_json_file_path):
            with open(self.wx_watermark_json_file_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["水印"] = {
            "is_admin": False,
            "alias": [],
            "summary": "添加水印",
            "usage": (
                "!水印 <信息1> <信息2> <信息3>"
                " - 三条信息以空格分割"
            ),
            "description": "为图片添加水印, 方便交青年大学习什么的截图。所以三个信息基本对应着 班级 姓名 学号。设置完成后直接发图片即可, 提示语以`[PictureForAddWatermark]`开头"
        }

    @on(GetQQPersonCommand)
    def add_watermark(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not message.startswith("水印"):
            return
        if message.startswith("水印"):
            message = message[2:].strip()
        event.prevent_postorder()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        sender_id = kwargs["sender_id"]
        params = message.split()

        if params == []:
            reply = "[PictureForAddWatermark] 为图片添加水印~\n可用以下命令设置预留水印(信息数≤3):\n[!水印 <信息1> <信息2> <信息3>]"
            cqhttp.sendPersonMessage(sender_id, reply)
            return

        modify_params = ' '.join(params[:3]).strip()
        logging.debug(
            f"插件[PictureForAddWatermark] 收到私聊指令, 更改预留水印…[用户id: {sender_id}]")
        with open(self.qq_watermark_json_file_path, "r+", encoding="utf-8") as f:
            watermark_data = json.load(f)
            watermark_data[str(sender_id)] = modify_params
            f.seek(0)
            f.truncate()
            json.dump(watermark_data, f, ensure_ascii=False)
        reply = f"[PictureForAddWatermark] 设置预留水印成功~\n[{modify_params}]"

        cqhttp.sendPersonMessage(sender_id, reply)

    @on(GetQQPersonCommand)
    def add_watermark(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not message.startswith("水印"):
            return
        if message.startswith("水印"):
            message = message[2:].strip()
        event.prevent_postorder()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        cqhttp.sendGroupMessage(kwargs["group_id"], "[bot] 群聊暂不支持此命令")

    @on(GetWXCommand)
    def add_watermark(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if not message.startswith("水印"):
            return
        if message.startswith("水印"):
            message = message[2:].strip()
        event.prevent_postorder()
        wcf: Wcf = self.emit(Events.GetWCF__)
        if kwargs["roomid"]:
            wcf.send_text(f"[bot] 群聊暂不支持此命令", kwargs["roomid"])
            return
        sender = kwargs["sender"]
        params = message.split()

        if params == []:
            reply = "[PictureForAddWatermark] 为图片添加水印~\n可用以下命令设置预留水印(信息数≤3):\n[!水印 <信息1> <信息2> <信息3>]"
            wcf.send_text(reply, sender)
            return

        modify_params = ' '.join(params[:3]).strip()
        logging.debug(
            f"插件[PictureForAddWatermark] 收到私聊指令, 更改预留水印…[用户id: {sender}]")
        with open(self.wx_watermark_json_file_path, "r+", encoding="utf-8") as f:
            watermark_data = json.load(f)
            watermark_data[sender] = modify_params
            f.seek(0)
            f.truncate()
            json.dump(watermark_data, f, ensure_ascii=False)
        reply = f"[PictureForAddWatermark] 设置预留水印成功~\n[{modify_params}]"

        wcf.send_text(reply, sender)

    @on(QQ_private_message)
    def picture_for_add_watermark(self, event: EventContext, **kwargs):
        config = self.emit(Events.GetConfig__)
        message: PersonMessage = kwargs["QQevents"]

        # 忽略自身消息
        if message.sender == config.qq:
            return

        # 此处只处理图片消息
        if not (message.message[0].type == "Image" and
                message.message[0].url):
            return

        event.prevent_postorder()
        sender_id = message.user_id
        sender_id_str = str(sender_id)
        image_url = message.message[0].url
        cqhttp: CQHTTP_Protocol = self.emit(GetCQHTTP__)
        tmp_id = cqhttp.sendPersonMessage(
            sender_id, "[PictureForAddWatermark] 获取到图片, 正在为图片添加水印…\n可用以下命令设置预留水印(信息数≤3):\n[!水印 <信息1> <信息2> <信息3>]"
        ).message_id
        logging.debug(
            f"插件[PictureForAddWatermark]获取到图片, 正在为图片添加水印…[用户: {sender_id}][图片链接: {image_url}]")

        try:
            response = requests.get(image_url)
            image_content = response.content

            # 处理调色板模式到RGB模式
            image = Image.open(io.BytesIO(image_content))
            image = image.convert('RGB')
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes = image_bytes.getvalue()

            with open(self.qq_watermark_json_file_path, "r", encoding="utf-8") as f:
                watermark_data: dict[str, str] = json.load(f)
            if sender_id_str in watermark_data:
                image = add_text_to_image(
                    image_bytes, watermark_data[sender_id_str].split(' '))
            else:

                image = add_text_to_image(
                    image_bytes,
                    [cqhttp.getStrangerInfo(sender_id).nickname]
                )
        except Exception as e:
            image = f"[PictureForAddWatermark]err: {e}"
        if isinstance(image, str):
            cqhttp.sendPersonMessage(sender_id, image)
        else:
            cqhttp.sendPersonMessage(sender_id, image.toString())
        cqhttp.recall(tmp_id)
        return

    @on(Wx_msg)
    def picture_for_add_watermark(self, event: EventContext, **kwargs):
        message: WxMsg = kwargs["Wx_msg"]
        wcf: Wcf = self.emit(Events.GetWCF__)

        # 此处只处理图片消息
        if message.type != 3:
            return

        # 忽略自身消息
        if message.sender == wcf.self_wxid:
            return

        # 忽略群消息
        if message.from_group():
            return

        event.prevent_postorder()
        sender = message.sender
        image_path = wcf.download_image(
            message.id,
            message.extra,
            os.path.join(os.path.dirname(__file__), "cache")
        )
        wcf.send_text(
            "[PictureForAddWatermark] 获取到图片, 正在为图片添加水印…\n可用以下命令设置预留水印(信息数≤3):\n[!水印 <信息1> <信息2> <信息3>]", sender)
        logging.debug(
            f"插件[PictureForAddWatermark]获取到图片, 正在为图片添加水印…[用户: {sender}][图片链接: {image_path}]")

        try:
            # 从本地路径读取图像文件成字节码
            with open(image_path, 'rb') as f:
                image_content = f.read()

            # 处理调色板模式到RGB模式
            image = Image.open(io.BytesIO(image_content))
            image = image.convert('RGB')
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes = image_bytes.getvalue()

            with open(self.wx_watermark_json_file_path, "r", encoding="utf-8") as f:
                watermark_data: dict[str, str] = json.load(f)
            if sender in watermark_data:
                image = add_text_to_image(
                    image_bytes, watermark_data[sender].split(' '))
            else:
                friend = wcf.get_info_by_wxid(sender)
                image = add_text_to_image(
                    image_bytes,
                    [friend['name']]
                )
        except Exception as e:
            image = f"[PictureForAddWatermark]err: {e}"
        finally:
            os.remove(image_path)
        if isinstance(image, str):
            wcf.send_text(image, sender)
        else:
            wcf.send_image(
                os.path.join(os.path.dirname(__file__), "temp.jpg"),
                sender
            )
        return
