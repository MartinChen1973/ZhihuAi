# 利用封装的SemanticKernel.SkUtilities快速创建应用。
import asyncio
from SemanticKernel.SkUtilities.SkUtility import SkUtility
from semantic_kernel.core_skills.time_skill import TimeSkill
# from semantic_kernel.core_skills.time_skill import TimePlugin # 这个TimePlugin是旧的，不要用了

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    kernel.import_skill(TimeSkill(), "time")

    ThePromptTemplate = """
    Answer to the following questions using JSON syntax, including the data used.
    
    Today is: {{time.Date}}
    Current time is: {{time.Time}}
    Is it morning, afternoon, evening, or night (morning/afternoon/evening/night)?
    Is it weekend time (weekend/work day)?
    """

    myKindOfDay = kernel.create_semantic_function(ThePromptTemplate, max_tokens=350)

    myOutput = await myKindOfDay.invoke_async()
    print(myOutput)


if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())