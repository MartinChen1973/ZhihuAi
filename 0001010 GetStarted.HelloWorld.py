# 这个例子演示如何向用户输出“Hello World!”，并讲述一个相关的笑话。
# 在运行之前，请确保上一课程中的.env已经正确配置
# 如果使用vscode，可以直接点右上角三角形运行此脚本

import os
from openai import OpenAI

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# 基于 prompt 生成文本
prompt = """
向用户说“Hello World!”，然后换行，并讲述一个相关的笑话。
"""
## 以下是一个简单的函数（或者叫“方法”），用来调用大模型生成文本
def get_completion(prompt, model="gpt-3.5-turbo"):      # 默认使用 gpt-3.5-turbo 模型
    messages = [{"role": "user", "content": prompt}]    # 将 prompt 作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,                                  # 模型输出的随机性，0 表示随机性最小
    )
    if response is not None:
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content          # 返回模型生成的文本
            # 处理生成的文本
        else:
            print("No choices in response")
            print(response)
    else:
        print("No response received")

# 调用大模型
response = get_completion(prompt)

print(response)