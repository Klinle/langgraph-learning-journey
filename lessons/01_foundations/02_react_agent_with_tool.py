import sys
import os
from langchain_core.tools import tool

# 将项目根目录添加到系统路径，确保可以导入 config 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.llm import get_llm
from langgraph.prebuilt import create_react_agent

# 1. 定义一个简单的自定义工具 (Tools)
# 使用 @tool 装饰器定义，Docstring 非常重要，因为它是大模型判断何时调用该工具的依据。
@tool
def multiply(a: int, b: int) -> int:
    """计算两个整数的乘积。当需要做乘法运算时使用此工具。"""
    print(f"\n[Tool Execution] 正在执行乘法工具: {a} * {b}...")
    return a * b

# 2. 初始化大语言模型与绑定工具
try:
    # 获取我们在 config 模块中统一配置的 LLM
    llm = get_llm(temperature=0)
except ValueError as e:
    print(f"提示: {e}")
    print("在未配置 API Key 的情况下，以下代码仅作为结构参考，无法实际调用模型。")
    llm = None

tools = [multiply]

# 3. 创建预置的 ReAct Agent
# create_react_agent 会自动为我们构建包含：
# - 决定是否调用工具的 Agent 节点
# - 执行工具 of Tool 节点
# - 根据执行结果反馈给 Agent 的循环条件边
if llm is not None:
    agent_executor = create_react_agent(llm, tools)

if __name__ == "__main__":
    if llm is None:
        print("请在 `.env` 中填写正确的 API KEY 后运行本脚本以进行模型测试。")
        sys.exit(0)

    print("启动内置 ReAct Agent 实例...")
    user_query = "请帮我计算一下 37 乘以 84 是多少？"
    print(f"用户问题: {user_query}")
    
    # 运行 Agent 
    response = agent_executor.invoke({"messages": [("user", user_query)]})
    
    print("\n--- 最终执行结果 ---")
    # messages 列表中最后一个消息就是 Agent 的最终回复
    final_message = response["messages"][-1]
    print(f"Agent 回复: {final_message.content}")
