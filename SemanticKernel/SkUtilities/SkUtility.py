import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import os

class SkUtility:

    # 创建LLM模型，并加载 .env 到环境变量（包括自动修改base_url）
    @staticmethod
    def createCompletionService(model_version: str = "gpt-3.5-turbo") -> OpenAIChatCompletion:

        # 加载 .env 到环境变量 ==========================
        from dotenv import load_dotenv, find_dotenv
        _ = load_dotenv(find_dotenv())

        # 配置LLM model也就是 OpenAI 服务。OPENAI_BASE_URL 会被自动加载生效 ==========================
        api_key = os.getenv('OPENAI_API_KEY')
        model = OpenAIChatCompletion(
            model_version,
            api_key,
        )
        # 注意，由于上面一个方法中自动使用了OpenAi的url（https://api.openai.com/v1/）且无法设置
        # 所以如果用的不是OpenAi，需要手动设置一下base_url参数
        model.client.base_url = os.getenv('OPENAI_API_BASE')
        return model

    # 创建 semantic kernel，并为其自动创建LLM服务
    @staticmethod
    def createKernelWithCompletion(completionName: str = "my-gpt3", model_version: str = "gpt-3.5-turbo") -> sk.Kernel:

        # 创建 semantic kernel
        kernel = sk.Kernel()

        # 创建LLM 服务并将其加入 kernel。可以加多个。
        # 第一个加入的会被默认使用，非默认的要被指定使用
        model = SkUtility.createCompletionService(model_version)
        kernel.add_text_completion_service(completionName, model)
        return kernel
