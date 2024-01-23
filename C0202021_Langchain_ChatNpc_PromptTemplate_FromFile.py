# 这个例子演示了如何把 Langchain PromptTemplate存储在文件中，以方便线上调试。
# 安装 Langchain: pip install langchain==0.1.0 
# 安装OpenAi扩展：pip install langchain-openai # v0.1.0新增的底包
# 安装Yaml读写支持：pip install PyYAML （这是为了加载人物的数值，如果只是使用load_prompt，无需安装）

import asyncio
from langchain_openai import ChatOpenAI
from langchain.prompts import load_prompt
from Langchain.chatNpc.entities.npc import Npc
import json

async def main():

    # 加载 .env 到环境变量，并创建OpenAI的API实例
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())
    llm = ChatOpenAI()

    # 从文件加载模板、人物数据
    template = load_prompt("./Langchain/chatNpc/prompts/chatNpc_system.yaml")
    daxiong = Npc(**json.load(open("./Langchain/chatNpc/entities/chatNpc_daxiong.json")))
    panghu = Npc(**json.load(open("./Langchain/chatNpc/entities/chatNpc_panghu.json")))

    # 第一个问题由胖虎发起。此问题可以从一个随机的问题列表中选取，或用另外一个ai程序自动生成。
    last_query = "你怎么还没做完作业？快点做，我要抄。"
    print(panghu.name + ": ", last_query)

    def answer(npc, another_npc, query):
        prompt = template.format(
            npc_name=npc.name,
            charactor=npc.charactor,
            description = npc.description,
            another_npc_name= another_npc.name,
            query = query
        )
        response = llm.invoke(prompt)
        return response.content
    
    for i in range(2):

        # 大雄回答
        last_query = answer(daxiong, panghu, last_query)
        print(daxiong.name + ": ", last_query)

        # 胖虎回答
        last_query = answer(panghu, daxiong, last_query)
        print(panghu.name + ": ", last_query)

if __name__ == "__main__":
    asyncio.run(main())