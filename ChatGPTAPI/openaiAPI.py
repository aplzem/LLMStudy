import openai

# 设置你的 OpenAI API 密钥
openai.api_key = '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'

# 多轮对话
# def multi_conversation():
#     conversation = []
#     while True:
#         # 获取用户输入
#         user_input = input("User: ")
#         # 设定退出条件
#         if user_input == 'exit':
#             break
#         # 发送对话请求
#         user_chat = {'role': 'user', 'content': user_input}
#         conversation.append(user_chat)
#         response = openai.ChatCompletion.create(
#             model="davinci",
#             messages=conversation,
#         )
#         # 提取助手的回复
#         assistant_reply = response.choices[0].text
#         print("Assistant:", assistant_reply)
#         # 更新对话历史
#         # conversation.append({'role': 'user', 'content': user_input})
#         conversation.append({'role': 'assistant', 'content': assistant_reply})
if __name__ == '__main__':
    conversation = []
    while True:
        # 获取用户输入
        user_input = input("User: ")
        # 设定退出条件
        if user_input == 'exit':
            print("Bye!")
            print(conversation)
            break
        # 发送对话请求
        user_chat = {'role': 'user', 'content': user_input}
        conversation.append(user_chat)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
        )
        # 提取助手的回复
        assistant_reply = response.choices[0].message.content
        # reply = bytes(assistant_reply, 'utf-8').decode('unicode_escape')
        print("Assistant:", assistant_reply)
        # 更新对话历史
        # conversation.append({'role': 'user', 'content': user_input})
        conversation.append({'role': 'assistant', 'content': assistant_reply})

