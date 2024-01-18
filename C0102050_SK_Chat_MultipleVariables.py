# 展示如何在调用Semantic Function的时候，传入多个变量。
import asyncio
import semantic_kernel as sk
from SemanticKernel.SkUtilities.SkUtility import SkUtility

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    # 用prompt生成一个Chat方法
    prompt = """对话历史如下:
    {{$history}}
    ---
    User: {{$request}}
    Assistant:  """

    chat_function = kernel.create_semantic_function(prompt)
    print(chat_function.model_dump_json())

    history = []

    while True:
        request = input("User > ").strip()
        if not request:
            break

        # 通过 ContextVariables 维护多个输入变量
        variables = sk.ContextVariables()
        variables["request"] = request
        variables["history"] = "\n".join(history)

        response = await kernel.run_async(
            chat_function,
            input_vars=variables, # 注意这里从 input_str 改为 input_vars
        )
        print(response.model_dump_json())

        # 将新的一轮添加到 history 中
        history.append("User: " + request)
        history.append("Assistant: " + response.result)

        print("Assistant > " + response.result)


if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())