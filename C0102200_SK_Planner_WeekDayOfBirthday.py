# 展示如何使用语义内核SK的规划Planner功能。
# 此案例需要获取Bing Api Key。请参考：https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-text-how-to-signup
# 大致步骤如下：
# 1. 登录Azure Portal（需要有微软账号）
# 2. 如果以前没买过Azure服务，可以选这个：Start with an Azure free trial （Get $200 free credit toward Azure products and services, plus 12 months of popular free services.）
# 3. 前往marketplace，https://portal.azure.com/#view/Microsoft_Azure_Marketplace/MarketplaceOffersBlade/selectedMenuItemId/home
# 4. 搜索Bing，选择Bing Search v7，点击创建
# 4. 创建完成后，前往资源列表，找到刚刚创建的Bing Search v7，点击左侧的“密钥和终结点”，在弹出的窗口中找到“密钥1”，点击复制
# https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/Microsoft.BingSearch/selectionMode~/false/resourceGroupId//resourceGroupLocation//dontDiscardJourney~/false/selectedMenuId/home/launchingContext~/%7B%22galleryItemId%22%3A%22Microsoft.BingSearch%22%2C%22source%22%3A%5B%22GalleryFeaturedMenuItemPart%22%2C%22VirtualizedTileDetails%22%5D%2C%22menuItemId%22%3A%22home%22%2C%22subMenuItemId%22%3A%22Search%20results%22%2C%22telemetryId%22%3A%22c6859b70-ec47-4319-8f9c-c8e195ab443b%22%7D/searchTelemetryId/486e1895-5b43-4647-b437-3a8ffd926a5e
# 注意！：SK的很多core skills正在开发中。在本例子创建的时候（2024-1-17），Math只支持加法、减法。
import asyncio
from SemanticKernel.SkUtilities.SkUtility import SkUtility

from semantic_kernel.core_skills import FileIOSkill, MathSkill, TextSkill, TimeSkill
from semantic_kernel.planning import ActionPlanner

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    # 获取生日的函数
    parse_birthday_prompt = """
    抽取下述输入文本中第一个出现的日期。

    ---输入文本开始---
    {{$input}}
    ---输入文本结束---

    以YYYY-MM-DD格式输出日期。
    不要评论，不要分析，直接给出答案。
    """
    kernel.create_semantic_function(
        parse_birthday_prompt,
        function_name="parseDate",
        skill_name="DateParser",
        description="抽取输入文本中的日期"
    )

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