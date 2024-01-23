# 这个例子演示了如何从LLM返回的文字中使用PydanticOutputParser“精准提取”特定的数据。
# 安装 Langchain: pip install langchain==0.1.0 
# 安装OpenAi扩展：pip install langchain-openai # v0.1.0新增的底包
# 安装Yaml读写支持：pip install PyYAML （这是为了加载人物的数值，如果只是使用load_prompt，无需安装）

import asyncio
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from LangchainData.Parser.Date import DateValidated
from datetime import datetime

async def main():

    # 加载 .env 到环境变量
    from  dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())
    model = ChatOpenAI(temperature=0)

    # 根据Pydantic对象的定义，构造一个OutputParser
    parser = PydanticOutputParser(pydantic_object=DateValidated)
    # parser = PydanticOutputParser(pydantic_object=datetime)

    template = """提取用户输入中的日期。
    {format_instructions}
    用户输入:
    {query}"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
        # 直接从OutputParser中获取输出描述，并对模板的变量预先赋值
        partial_variables={"format_instructions": parser.get_format_instructions()} 
    )

    print("====Format Instruction=====")
    print(parser.get_format_instructions())

    query = "2023年四月6日天气晴..."
    model_input = prompt.format_prompt(query=query)

    print("====Prompt=====")
    print(model_input.to_string())

    output = model(model_input.to_messages())
    print("====模型原始输出=====")
    print(output)
    print("====Parse后的输出=====")
    date = parser.parse(output.content)
    print(date)

if __name__ == "__main__":
    asyncio.run(main())