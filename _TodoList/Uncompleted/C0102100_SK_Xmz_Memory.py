# 展示如何在调用Semantic Function的时候，传入多个变量。
import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding
from SemanticKernel.SkUtilities.SkUtility import SkUtility
import os

async def main():

    kernel = SkUtility.createKernelWithCompletion()

    # 从txt文件读取所有内容，并按行分拆
    with open("./app_data/xmz.txt", "r", encoding="utf-8") as f:
        text = f.read()
        lines = text.split("\n")

    # 添加 embedding 服务
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv())
    embedding = OpenAITextEmbedding("text-embedding-ada-002", os.getenv('OPENAI_API_KEY'));
    embedding.client.base_url = os.getenv('OPENAI_API_BASE')
    kernel.add_text_embedding_generation_service("ada", embedding)
    
    # 注册一个内存存储
    kernel.register_memory_store(memory_store=sk.memory.VolatileMemoryStore())
    # 将分片后的内容，存入内存
    for index, line in enumerate(lines):
        await kernel.memory.save_information_async("chatall", id=index, text=line)

    # 向量搜索
    query = input("你想问什么呢？")
    result = await kernel.memory.search_async("chatall", query)
    print(result[0].text)
    
if __name__ == "__main__":
# Run the main asynchronous function
    asyncio.run(main())