# ---------------------------------------------模型参数---------------------------------------------

# [必需] OpenAI的配置, api_key: OpenAI的API Key
# 1.若只有一个api-key, 请直接修改以下内容中的"openai_api_key"为你的api-key
# 2.如准备了多个api-key, 可以以字典的形式填写, 程序会自动选择可用的api-key
# 字典的键可随意命名, 字典的值为配置字典
# 若全为默认配置, 可直接将值设定为`api_key`
# 默认配置在下方`completion_api_params`字段中修改

# 3.（非必要选择！）现已支持网络代理，格式："http_proxy": "http://127.0.0.1:7890"   其中7890是你代理软件打开的端口，一般开全局则无需设置
# 4.（非必要选择！）现已支持反向代理，可以添加reverse_proxy字段以使用反向代理，使用反向代理可以在国内使用OpenAI的API，反向代理的配置请参考 ，https://github.com/Ice-Hazymoon/openai-scf-proxy , 格式为： "reverse_proxy": "http://example.com:12345/v1"

# 此处为默认配置, 即启用此api key后默认启用此配置
# 但支持用`!reset -<键值>`切换单个session的配置, 或者仅用`!talk`切换单轮对话的配置
# 具体请看`!cmd reset`和`!cmd talk`

openai_config = {
    # "example1": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 全为默认配置, 填写字符串即可

    # "example2": {
    #     "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    #     "params": {  # 配置此api默认参数, 此处不建议启用4.0模型, token消耗过快。可用`!cmd reset`查看临时切换模型规则
    #         "model": "gpt-4-0314",
    #         "temperature": 0.8,
    #         "top_p": 1,
    #         "frequency_penalty": 0.3,
    #         "presence_penalty": 1.0,
    #     },
    #     "http_proxy": None,     # 代理, 默认None
    #     "reverse_proxy": None,  # 反向代理, 默认None
    #     "is_plus": True,        # 是否为付费模型, 默认False。此字段会判断是否支持切换到4.0模型, 若所有api都为False则抛出无api可用
    # },
}


# OpenAI补全API的参数, OpenAI的文档: https://beta.openai.com/docs/api-reference/completions/create
# 请在下方填写模型, 程序自动选择接口,现已支持的模型有:
#    'gpt-4'	             -->新出的更强4.0接口, 目前版本似乎仅plus会员等可用
#    'gpt-4-0314'
#    'gpt-4-32k'
#    'gpt-4-32k-0314'
#    'gpt-3.5-turbo'                -->这个是默认的3.5接口, 使用方法复制到下面的"model": xxx  , 替换xxx
#    'gpt-3.5-turbo-0301'
#    'text-davinci-003'             -->这个是原来的3.0接口, 人格相对好设置, 但是token收费会更高
#    'text-davinci-002'
#    'code-davinci-002' | 'code-cushman-001' | 'text-curie-001' | 'text-babbage-001' | 'text-ada-001'   ....等等、还有一些你可能用不到的模型
completion_api_params = {
    "default": {  # 默认配置
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,  # 数值越低得到的回答越理性, 取值范围[0, 1]
        "top_p": 1,  # 生成的文本的文本与要求的符合度, 取值范围[0, 1]
        "frequency_penalty": 0.3,
        "presence_penalty": 1.0,
    },
    "gpt4": {  # 在`!cmd reset`或者`!cmd talk`中查看用法
        "model": "gpt-4-0314",
        "temperature": 0.8,
        "top_p": 1,
        "frequency_penalty": 0.3,
        "presence_penalty": 1.0,
    },
}


# 消息处理的超时时间, 单位为秒
process_message_timeout = 180


# 每次向OpenAI接口发送对话记录上下文的字符数
# 注意: 较大的prompt_submit_length会导致OpenAI账户额度消耗更快
# 3.5模型只支持到4096
prompt_submit_length = 4096


# 每个会话的过期时间, 单位为秒, 原默认值20分钟, 即 1200 ,注意这里的数字只能是整数
session_expire_time = 600000


# 消息超时提示
reply_timeout_message = "【检测到时空风暴影响，返回信号被确认超时】"
