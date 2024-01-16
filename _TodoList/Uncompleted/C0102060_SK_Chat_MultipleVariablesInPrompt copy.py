# coding=utf-8
# 这个例子演示了如何使用 semantic kernel 来把自然语言转换成Dos命令行，且分离存放Prompt和Config文件
# 安装 semantic kernel: pip install semantic-kernel
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os

async def main():

    # 加载 .env 到环境变量 ==========================
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())

    # 配置LLM model也就是 OpenAI 服务。OPENAI_BASE_URL 会被自动加载生效 ==========================
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

    from typing import List

    # 从目录中导入 semantic function。目录中必须包含prompt.txt和config.json
    # 所有config和prompt 都是coding=utf-8
    my_skills = kernel.import_semantic_skill_from_directory(
        "./SemanticKernel", "SemanticFunctions")

    history = []

    async def run_while():
        while True:
            request = input("User > ").strip()
            
            if not request:
                break
            if (request == "print"):
                print(history)
                continue

            # 通过 ContextVariables 维护多个输入变量
            variables = sk.ContextVariables()
            variables["request"] = request
            variables["history"] = "\n".join(history)

            print(variables)

            history.append("User: " + request)
            # time_out = 30 
            # try:
            result = await run_function(variables) # wait for n seconds
            # except asyncio.TimeoutError:
            #     print(f"System > timeout({time_out}s). ")
            #     continue

            # 如果没超时，将新的一轮添加到 history 中
            if (result is None):
                print(f"System > result is None. ")
                continue

            # print(result)
            # 打印result 的json格式
            print(result.model_dump_json())

            history.append("Assistant: " + result.result)
            print("Assistant > " + result.result + "（直接回车退出对话）")

    asyncio.run(run_while())

    # 定义异步运行 function 的方法
    async def run_function(variables: sk.ContextVariables):
        return await kernel.run_async(
                my_skills["Chat"],
                input_vars=variables, # 注意这里从 input_str 改为 input_vars
        )

import asyncio
if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())