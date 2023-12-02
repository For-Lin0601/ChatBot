from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/sign', methods=['POST'])
def sign():
    # 在这里实现签名逻辑，这里只是一个简单的示例
    api_key = '114514'
    authorization = 'Bearer 114514'
    return jsonify({'api_key': api_key, 'authorization': authorization})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5700)
    # 阻塞
