# coding=utf-8
# 这个例子演示了如何使用 semantic kernel 来把自然语言转换成Dos命令行，且分离存放Prompt和Config文件
# 安装 semantic kernel: pip install semantic-kernel
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os
import asyncio

# 创建LLM模型，并加载 .env 到环境变量（包括自动修改base_url）
def createCompletion(model_version: str = "gpt-3.5-turbo") -> OpenAIChatCompletion:

    # 加载 .env 到环境变量 ==========================
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())

    # 配置LLM model也就是 OpenAI 服务。OPENAI_BASE_URL 会被自动加载生效 ==========================
    api_key = os.getenv('OPENAI_API_KEY')
    model = OpenAIChatCompletion(
        model_version,
        api_key,
    )
    # 注意，由于上面一个方法中自动使用了OpenAi的url（https://api.openai.com/v1/）且无法设置
    # 所以如果用的不是OpenAi，需要手动设置一下base_url参数
    model.client.base_url = os.getenv('OPENAI_API_BASE')
    return model

def createKernelWithCompletion(completionName: str = "my-gpt3", model_version: str = "gpt-3.5-turbo") -> sk.Kernel:

    # 创建 semantic kernel
    kernel = sk.Kernel()

    # 创建LLM 服务并将其加入 kernel。可以加多个。
    # 第一个加入的会被默认使用，非默认的要被指定使用
    model = createCompletion(model_version)
    kernel.add_text_completion_service(completionName, model)
    return kernel

async def main():

    kernel = createKernelWithCompletion()

    # 从目录中导入 semantic function。目录中必须包含prompt.txt和config.json
    my_skills = kernel.import_semantic_skill_from_directory(
        "./SemanticKernel", "SemanticFunctions")
    print(my_skills.keys())

    # 运行 function 看结果
    async def run_function(input_str: str):
        return await kernel.run_async(
            my_skills["LinuxCommand"],
            my_skills["DosCommand"],
            input_str = input_str,
        )

    # 注意这里直接使用 await 如果你在本地运行请执行：asyncio.run(run_function())
    input_str = input("你想执行什么指令呢？")
    result = await asyncio.wait_for(run_function(input_str), 10) # wait for n seconds
    # result = await run_function(input_str) # wait for ever
    print(result)

if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())