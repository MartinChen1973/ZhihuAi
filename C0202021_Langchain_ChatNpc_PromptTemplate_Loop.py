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

    template_text = """
        你是游戏中的NPC，名字叫{npc_name}，你的性格是{charactor}。
        你在回答问题时的语气总是与性格相匹配。
        每次回答要言简意赅，尽量不超过50个汉字。
        直接给出答案，不要写角色的名字，也不要分析、注释。
    """
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(template_text),
            HumanMessagePromptTemplate.from_template("{another_npc_name}对你说：{query}，你会怎样回答？"),
        ]
    )

    last_query = "你怎么还没做完作业？快点做，我要抄。"
    print("胖虎：", last_query)

    for i in range(3):

        # 大雄回答
        prompt_daxiong = template.format_messages(
            npc_name="大雄",
            charactor="善良，胆小，平时最害怕胖虎。",
            another_npc_name="胖虎",
            query = last_query
        )
        response = llm.invoke(prompt_daxiong)
        print("大雄：", response.content)
        last_query = response.content

        # 胖虎回答
        prompt_panghu = template.format_messages(
                npc_name="胖虎",
                charactor="粗鲁，没礼貌，莽撞，爱欺负人，平时最爱欺负大雄。",
                another_npc_name="大雄",
                query = last_query
            )
        response = llm.invoke(prompt_panghu)
        print("胖虎：", response.content)
        last_query = response.content

if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())