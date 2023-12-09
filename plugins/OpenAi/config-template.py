# ---------------------------------------------模型参数---------------------------------------------

# [必需] OpenAI的配置，api_key: OpenAI的API Key
# 1.若只有一个api-key，请直接修改以下内容中的"openai_api_key"为你的api-key
# 2.如准备了多个api-key，可以以列表的形式填写，程序会自动选择可用的api-key
openai_api_keys = [
    # "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",  # 第一个，用完了
    # "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",  # 第二个，传说120刀，封咯
    # "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",  # 第三个，用完了
    # "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",  # 第四个，同时WeCHatGPT也在用，封咯
    # "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",  # 第五个，用完了
    # "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",  # 封了
    # "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",  # 封了
    # "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",  # 用完
    "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",
    "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",  # 用完
    "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",
    "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",
]


# OpenAI补全API的参数，OpenAI的文档: https://beta.openai.com/docs/api-reference/completions/create
# 请在下方填写模型，程序自动选择接口,现已支持的模型有：
#    'gpt-4'	             -->新出的更强4.0接口，目前版本似乎仅plus会员等可用
#    'gpt-4-0314'
#    'gpt-4-32k'
#    'gpt-4-32k-0314'
#    'gpt-3.5-turbo'                -->这个是默认的3.5接口，使用方法复制到下面的"model"：xxx  ，替换xxx
#    'gpt-3.5-turbo-0301'
#    'text-davinci-003'             -->这个是原来的3.0接口，人格相对好设置，但是token收费会更高
#    'text-davinci-002'
#    'code-davinci-002' | 'code-cushman-001' | 'text-curie-001' | 'text-babbage-001' | 'text-ada-001'   ....等等、还有一些你可能用不到的模型
completion_api_params = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.8,  # 数值越低得到的回答越理性，取值范围[0, 1]
    "top_p": 1,  # 生成的文本的文本与要求的符合度, 取值范围[0, 1]
    "frequency_penalty": 0.3,
    "presence_penalty": 1.0,
}


# 消息处理的超时时间，单位为秒
process_message_timeout = 180


# 每次向OpenAI接口发送对话记录上下文的字符数
# 注意：较大的prompt_submit_length会导致OpenAI账户额度消耗更快
prompt_submit_length = 4096


# 每个会话的过期时间，单位为秒，原默认值20分钟，即 1200 ,注意这里的数字只能是整数
session_expire_time = 600000
