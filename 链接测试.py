# from nakuru import (
#     CQHTTP,
#     GroupMessage
# )
# from nakuru.entities.components import Plain, Node, Image

# app = CQHTTP(
#     host="127.0.0.1",
#     port=6700,
#     http_port=5700,
#     token="114514"
# )

# @app.receiver("GroupMessage")
# async def _(app: CQHTTP, source: GroupMessage):
#     # 方法 1
#     await app.sendGroupForwardMessage(source.group_id, [
#         Node(name="落雪ちゃん", uin=2941383730, content=[
#             Plain(text="nc什么时候cos小老师")
#         ]),
#         Node(name="盐焗雾喵", uin=2190945952, content=[
#             Plain(text="今晚就cos小老师")
#         ]),
#         Node(name="Rosemoe♪ ~ requiem ~", uin=2073412493, content=[
#             Plain(text="好耶"),
#             Image.fromFileSystem("./src/1.jpg")
#         ])
#     ])
#     # 方法 2
#     await app.sendGroupForwardMessage(source.group_id, [
#         {
#             "type": "node",
#             "data": {
#                 "name": "落雪ちゃん",
#                 "uin": 2941383730,
#                 "content": "nc什么时候cos小老师"
#             }
#         },
#         {
#             "type": "node",
#             "data": {
#                 "name": "盐焗雾喵",
#                 "uin": 2190945952,
#                 "content": "今晚就cos小老师"
#             }
#         },
#         {
#             "type": "node",
#             "data": {
#                 "name": "Rosemoe♪ ~ requiem ~",
#                 "uin": 2073412493,
#                 "content": [
#                     {
#                         "type": "text",
#                         "data": {"text": "好耶"}
#                     },
#                     {
#                         "type": "image",
#                         "data": {"file": "file:///D:/src/1.jpg"}  # 此处需要绝对路径
#                     }
#                 ]
#             }
#         }
#     ])

# app.run()
import requests
from flask import Flask, request
from flask_socketio import SocketIO

class WebsocketCommunicator:
    def __init__(self):
        self.socketio = None
        self.server_address = 'http://127.0.0.1:6700'

    def start_listening(self):
        app = Flask(__name__)
        self.socketio = SocketIO(app)

        @self.socketio.on('message')
        def handle_message(data):
            if data.get('type') == 'text':
                # 执行插件逻辑或其他操作
                self.send_message(data.get('message'))
        
        @app.route('/')
        def index():
            return 'Websocket Listener Running'

        self.socketio.run(app)

    def send_message(self, message):
        payload = {'type': 'text', 'message': message}
        
        try:
            response = requests.post(f'{self.server_address}/send', json=payload)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f'Error sending message: {e}')
            return False


communicator = WebsocketCommunicator()
communicator.start_listening()