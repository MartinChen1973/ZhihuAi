import asyncio
from SemanticKernel.SkUtilities.SkUtility import SkUtility
from SemanticKernel.NativeFunctions.CommandVerifier import NormalCommandVerifier, NativeCommandVerifier

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    # 从目录中导入 semantic function。目录中必须包含prompt.txt和config.json
    create_command_skills = kernel.import_semantic_skill_from_directory(
        "./SemanticKernel", "SemanticFunctions")
    print(create_command_skills.keys())

    # 运行 function 看结果
    async def run_function(input_str: str):
        return await kernel.run_async(
            create_command_skills["LinuxCommand"],
            create_command_skills["DosCommand"],
            input_str = input_str,
        )

    # 注意这里直接使用 await 如果你在本地运行请执行：asyncio.run(run_function())
    input_str = input("你想执行什么指令呢？")
    create_command_response = await run_function(input_str)
    print(f"create_command_result is {create_command_response.result}")

    # 1. 使用普通的方法来验证
    verify_command_response = NormalCommandVerifier().verify(create_command_response.result)
    print(f"normal_verifier says: command {create_command_response.result} is {verify_command_response}")

    # 2. 使用 native function 来验证
    # 加载 native function
    verify_skill = kernel.import_skill(NativeCommandVerifier(), "Verifier")

    # 运行
    verify_command_response = await kernel.run_async(
        verify_skill["verifyCommand"], # 注意这里的用法, 此数值是@sk_function.name
        # input_str="dir",
        input_str = create_command_response.result
    )
    print(f"native_function_verifier says: command {create_command_response.result} is {verify_command_response.result}")
    
if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())