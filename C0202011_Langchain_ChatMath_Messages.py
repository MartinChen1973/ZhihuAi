# 这个例子演示了如何使用 Langchain 来搭建一个简单的讲笑话服务
# 安装 Langchain: pip install langchain==0.1.0 
# 安装OpenAi扩展：pip install langchain-openai # v0.1.0新增的底包
import asyncio
from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage, #等价于OpenAI接口中的assistant role
    HumanMessage, #等价于OpenAI接口中的user role
    SystemMessage #等价于OpenAI接口中的system role
)

async def main():

    # 加载 .env 到环境变量
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())

    llm = ChatOpenAI() # 默认是gpt-3.5-turbo

    messages = [
        SystemMessage(content="你是一个数学机器人，可以计算10以内的加减乘除法。其他问题请回答“抱歉这个问题超出了我的能力。"), 
        AIMessage(content="欢迎！"),
        HumanMessage(content="你好，我是小明。你是谁？"), 
    ]
    messages.append(AIMessage(content=llm.invoke(messages).content))
    print(messages[-1])

    messages.append(HumanMessage(content="请问一加二等于几？"))
    print(messages[-1])
    messages.append(AIMessage(content=llm.invoke(messages).content))
    print(messages[-1])

    messages.append(HumanMessage(content="那2乘以6呢？"))
    print(messages[-1])
    messages.append(AIMessage(content=llm.invoke(messages).content))
    print(messages[-1])

    messages.append(HumanMessage(content="猫和狗为什么总是打架？"))
    print(messages[-1])
    messages.append(AIMessage(content=llm.invoke(messages).content))
    print(messages[-1])

if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())