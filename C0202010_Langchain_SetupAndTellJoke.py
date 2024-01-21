# 这个例子演示了如何使用 Langchain 来搭建一个简单的讲笑话服务
# 安装 Langchain: pip install langchain==0.1.0 
# 安装OpenAi扩展：pip install langchain-openai # v0.1.0新增的底包
from langchain_openai import ChatOpenAI

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

llm = ChatOpenAI() # 默认是gpt-3.5-turbo

response = llm.invoke("请给我讲一个关于程序员的笑话")
print(response.content)