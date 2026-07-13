import sys
import os

def check_dependencies():
    print("=" * 50)
    print(" 开始检测 LangGraph 学习环境依赖配置")
    print("=" * 50)
    
    # 1. 检查 Python 版本
    print(f"[Python 版本] -> {sys.version}")
    
    # 2. 检查核心包导入与版本
    packages = ["langgraph", "langchain_core", "langchain_openai", "pydantic", "dotenv"]
    for pkg in packages:
        try:
            # 动态导入
            module = __import__(pkg)
            version = getattr(module, "__version__", "未知")
            # 处理特殊的嵌套导入版本获取，比如 dotenv 的是 __version__，或者是别的值
            if pkg == "dotenv":
                import dotenv
                version = getattr(dotenv, "__version__", "已成功导入")
            print(f"[依赖包检查] 导入成功: {pkg:<16} (版本: {version})")
        except ImportError:
            print(f"[依赖包检查] 导入失败: {pkg:<16} ❌ 请确认已正确构建并进入 Docker 容器！")

    # 3. 检查环境变量加载
    print("\n--- 环境变量检测 ---")
    openai_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE", "未配置，使用默认官方接口")
    tracing = os.getenv("LANGCHAIN_TRACING_V2", "false")
    
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("[Env] OPENAI_API_KEY: 未设置或使用的是占位符 ⚠️")
        print("  -> 提示: 所有的核心流程（StateGraph本身）可以正常运行和练习，但如果涉及 LLM 调用，会触发报错。请编辑 `.env` 文件填入有效密钥。")
    else:
        # 脱敏打印
        masked_key = openai_key[:6] + "..." + openai_key[-4:] if len(openai_key) > 10 else "***"
        print(f"[Env] OPENAI_API_KEY: 已配置 ({masked_key}) ✅")
        
    print(f"[Env] OPENAI_API_BASE: {api_base}")
    print(f"[Env] LangSmith 链路追踪: {'已启用 (推荐)' if tracing.lower() == 'true' else '未启用'}")

    # 4. 尝试加载统一配置之 LLM
    print("\n--- 大模型加载测试 ---")
    try:
        from config.llm import get_llm
        llm = get_llm(model_name="gpt-4o-mini")
        print(f"[LLM] ChatOpenAI 客户端初始化成功！ ✅")
    except Exception as e:
        print(f"[LLM] ChatOpenAI 初始化失败或跳过 ⚠️ 原因: {e}")

    print("=" * 50)
    print(" 依赖与环境检测完毕！")
    print("=" * 50)

if __name__ == "__main__":
    check_dependencies()
