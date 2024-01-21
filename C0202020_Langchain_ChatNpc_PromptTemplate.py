# 这个例子演示了如何使用 Langchain PromptTemplate来实现多参数调用。
# 安装 Langchain: pip install langchain==0.1.0 
# 安装OpenAi扩展：pip install langchain-openai # v0.1.0新增的底包
import asyncio
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate

async def main():

    # 加载 .env 到环境变量
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())
    llm = ChatOpenAI()

    template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template("你是游戏中的NPC，名字叫{npc_name}，你的性格是{charactor}，你在回答问题时的语气总是与性格相匹配。"),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    )

    prompt_daxiong = template.format_messages(
            npc_name="大雄",
            charactor="善良，胆小，平时最害怕胖虎。",
            query="你是谁？"
        )
    prompt_panghu = template.format_messages(
            npc_name="胖虎",
            charactor="粗鲁，没礼貌，莽撞，爱欺负人，平时最爱欺负大雄。",
            query="你是谁？"
        )

    response = llm.invoke(prompt_daxiong)
    print("大雄：", response.content)

    response = llm.invoke(prompt_panghu)
    print("胖虎：", response.content)

if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())