# 展示如何在调用Semantic Function的时候，传入多个变量。
import asyncio
import semantic_kernel as sk
from SemanticKernel.SkUtilities.SkUtility import SkUtility

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    # 用prompt生成一个Summarize方法
    summarize_prompt = """
    请将以下 User 与 Assistant 的对话生成一个简短的摘要。
    确保你的摘要中包含完整的信息。
    <dialog>
    {{$history}}
    </dialog>
    摘要：
    """
    summarize_function = kernel.create_semantic_function(
        summarize_prompt,
        function_name="summarize",
        skill_name="ChatHistorySkill",
        description="Summarize a dialogue history",
    )

    # 用prompt生成一个Chat方法
    chat_prompt = """User 与 Assistant 的对话历史摘要如下:
    {{ChatHistorySkill.summarize $history}}
    ---
    User: {{$request}}
    Assistant:
    """
    chat_function = kernel.create_semantic_function(chat_prompt)

    history = []

    while True:
        request = input("User > ").strip()
        if not request:
            break
        if request == "print":
            print(history)
            continue

        # 通过 ContextVariables 维护多个输入变量
        variables = sk.ContextVariables()
        variables["request"] = request
        variables["history"] = "\n".join(history)

        response = await kernel.run_async(
            chat_function,
            input_vars=variables, # 注意这里从 input_str 改为 input_vars
        )

        # 将新的一轮添加到 history 中
        history.append("User: " + request)
        history.append("Assistant: " + response.result)

        print("Assistant > " + response.result)

        summary = await kernel.run_async(
            summarize_function,
            input_vars=variables,
        )
        print("Summary > " + summary.result)


if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())