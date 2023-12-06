import openai

# 设置你的API密钥
api_key = "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"


# 初始化OpenAI客户端
openai.api_key = api_key

# 创建一个对话
conversation = []

# 开始对话
while True:
    user_input = input("You: ")  # 用户输入
    conversation.append({"role": "user", "content": user_input})

    # 发送对话到GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 使用GPT-3的对话模型
        messages=conversation
    )

    # 获取GPT-3的回复
    gpt_response = response['choices'][0]['message']['content']
    print(f"GPT-3: {gpt_response}")

    # 将GPT-3的回复添加到对话中
    conversation.append({"role": "assistant", "content": gpt_response})
