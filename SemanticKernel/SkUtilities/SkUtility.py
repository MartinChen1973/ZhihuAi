import importlib
import inspect
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

    @staticmethod
    def importAllSemanticFunctions(kernel: sk.Kernel, semanticFunctionsDir: str):
        # 从目录中导入 semantic function。目录中必须包含prompt.txt和config.json
        parent_folder = os.path.dirname(semanticFunctionsDir)
        current_folder = os.path.basename(semanticFunctionsDir)
        return kernel.import_semantic_skill_from_directory(
            parent_folder, current_folder)

    @staticmethod
    # def importAllNativeFunctions(kernel: sk.Kernel, nativeFunctionsDir: str):
    #     classes = SkUtility.import_classes_from_directory(nativeFunctionsDir)
    #     native_skills = []
    #     for cls in classes:
    #         native_skills.append(kernel.import_skill(cls(), cls.__name__))
    #     return native_skills
    
    @staticmethod
    def import_classes_from_directory(directory):
        classes = []
        
        for filename in os.listdir(directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove ".py" extension
                module_path = f"{directory}.{module_name}"
                print("~~~~~module_path is : " + module_path)

                try:
                    # Determine the package name dynamically
                    package_name = ".".join(directory.split(os.sep))
                    print("~~~~~package_name is : " + package_name)
                    module = importlib.import_module(module_path, package=package_name)
                    print("~~~~~module is : " + str(module))
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj):
                            classes.append(obj)
                except ImportError as e:
                    print(f"Error importing module {module_name}: {e}")

        return classes
    
    @staticmethod
    def find_classes_in_folder(folder_path) -> list[type]:
        classes = []
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".py") and file_name != "__init__.py":
                    module_name = os.path.splitext(file_name)[0]
                    module_path = os.path.join(root, file_name).replace(os.sep, ".")
                    print("~~~~~module_path is : " + module_path)
                    
                    try:
                        print(module_path)
                        module = importlib.import_module(module_path)
                        for name, obj in inspect.getmembers(module):
                            if inspect.isclass(obj):
                                classes.append(obj)
                    except ImportError as e:
                        print(f"Error importing module {module_name}: {e}")

        return classes
