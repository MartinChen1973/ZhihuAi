# 利用封装的SemanticKernel.SkUtilities快速创建应用。
import asyncio
from SemanticKernel.SkUtilities.SkUtility import SkUtility

async def main():

    kernel = SkUtility.createKernelWithCompletion()
    semantic_skills = SkUtility.importAllSemanticFunctions(kernel, "./SemanticKernel/SemanticFunctions")
    print(semantic_skills.keys())
    native_skills = SkUtility.importAllNativeFunctions(kernel, "./NativeFunctions")
    print(native_skills)

    # 运行 function 看结果
    async def run_function(input_str: str):
        return await kernel.run_async(
            semantic_skills["DosCommand"],
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