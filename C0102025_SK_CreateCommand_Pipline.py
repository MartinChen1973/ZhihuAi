# 此示例展示了如何使用 SemanticKernel 创建一个简单的指令执行 pipeline
# pipleline可以顺序执行多个 function，每个 function 的输入是上一个 function 的输出。
import asyncio
from SemanticKernel.SkUtilities.SkUtility import SkUtility
from SemanticKernel.NativeFunctions.CommandVerifier import NativeCommandVerifier

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    # 加载 semantic function。目录中必须包含prompt.txt和config.json
    create_command_skills = kernel.import_semantic_skill_from_directory(
        "./SemanticKernel", "SemanticFunctions")
    print(create_command_skills.keys())

    # 加载 native function
    verify_skill = kernel.import_skill(NativeCommandVerifier(), "Verifier")

    # 运行 pipline 看结果
    async def run_function(input_str: str):
        return await kernel.run_async(
            create_command_skills["DosCommand"],
            verify_skill["verifyCommand"],
            input_str = input_str,
        )

    # 注意这里直接使用 await 如果你在本地运行请执行：asyncio.run(run_function())
    input_str = input("你想执行什么指令呢？")
    pipline_response = await run_function(input_str)
    print(pipline_response.result)

if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())