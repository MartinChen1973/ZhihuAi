# 展示如何使用语义内核SK的规划Planner功能。
# 注意！：SK的很多core skills正在开发中。在本例子创建的时候（2024-1-17），Math只支持加法、减法。
import asyncio
from SemanticKernel.SkUtilities.SkUtility import SkUtility

from semantic_kernel.core_skills import FileIOSkill, MathSkill, TextSkill, TimeSkill
from semantic_kernel.planning import ActionPlanner

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    kernel.import_skill(MathSkill(), "math")
    kernel.import_skill(FileIOSkill(), "fileIO")
    kernel.import_skill(TimeSkill(), "time")
    kernel.import_skill(TextSkill(), "text")

    # create an instance of action planner.
    planner = ActionPlanner(kernel)

    # the ask for which the action planner is going to find a relevant function.
    # 注意！：SK的很多core skills正在开发中。在本例子创建的时候（2024-1-17），Math只支持加法、减法。
    # ask = "110 + 990"
    # ask = "What is the sum of 110 and 990?"
    ask = input("What's your question? I can answer questions like: What is the sum of 110 and 990?)")

    # ask the action planner to identify a suitable function from the list of functions available.
    plan = await planner.create_plan_async(goal=ask)

    # ask the action planner to execute the identified function.
    result = await plan.invoke_async()
    print(result)
    """
    Output:
    1100
    """


if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())