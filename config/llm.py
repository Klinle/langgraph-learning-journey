import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 自动加载当前目录或上层目录中的 .env 文件
load_dotenv()

def get_llm(model_name: str = "deepseek-v4-flash", temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """
    获取统一配置的大语言模型 (ChatOpenAI 实例)。
    
    参数:
        model_name (str): 模型名称，默认为 "deepseek-v4-flash"。
        temperature (float): 温度参数，默认为 0.0（最确定性的输出）。
        kwargs: 传递给 ChatOpenAI 的其他参数。
        
    返回:
        ChatOpenAI: 配置好的 ChatOpenAI 实例。
    """
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    # 智能推断：如果使用的是 deepseek 模型，且 API BASE 未被显式修改，则指向 deepseek 官方端点
    if "deepseek" in model_name.lower() and api_base == "https://api.openai.com/v1":
        api_base = "https://api.deepseek.com"
        
    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError(
            "未检测到有效的 API KEY。 "
            "请在项目根目录下的 `.env` 文件中填写您真实的 API Key，或在环境变量中配置。"
        )

        
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=api_key,
        openai_api_base=api_base,
        **kwargs
    )
