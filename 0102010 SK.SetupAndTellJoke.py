# 这个例子演示了如何使用 semantic kernel 来搭建一个简单的讲笑话服务
# 安装 semantic kernel: pip install semantic-kernel
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 配置LLM model也就是 OpenAI 服务。OPENAI_BASE_URL 会被自动加载生效
api_key = os.getenv('OPENAI_API_KEY')
model = OpenAIChatCompletion(
    "gpt-3.5-turbo",
    api_key,
)
# 注意，由于上面一个方法中自动使用了OpenAi的url（https://api.openai.com/v1/）且无法设置
# 所以如果用的不是OpenAi，需要手动设置一下base_url参数
model.client.base_url = os.getenv('OPENAI_API_BASE')

# 创建 semantic kernel
kernel = sk.Kernel()

# 把 LLM 服务加入 kernel
# 可以加多个。第一个加入的会被默认使用，非默认的要被指定使用
kernel.add_text_completion_service("my-gpt3", model)

import asyncio

# 定义 semantic function
# 参数由{{ }}标识
# prompt = "给我讲个关于{{$input}}的笑话吧"
# prompt = "给我推荐一个能补充{{$input}}的食物吧"
prompt = "给帮我推荐一个能治疗{{$input}}的药方吧"
tell_me_about = kernel.create_semantic_function(prompt)
# 等待用户输入要讲的笑话内容
# input_str = input("你想听什么笑话呢？")
# input_str = input("你想补充哪方面的营养呢？")
input_str = input("你想治疗什么疾病呢？")

# 运行 function 看结果
async def run_function():
    return await kernel.run_async(
        tell_me_about,
        input_str = input_str,
    )

# 注意这里直接使用 await 如果你在本地运行请执行：asyncio.run(run_function())
result = asyncio.run(run_function())
print(result)