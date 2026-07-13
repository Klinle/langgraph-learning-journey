import sys
import os
import asyncio
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# 将项目根目录添加到系统路径，确保可以导入 config 模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.llm import get_llm

# 1. 定义消息 State
class MessageState(TypedDict):
    prompt: str
    reply: str

# 2. 初始化大语言模型
try:
    # 获取 ChatOpenAI 模型，流式传输需要模型支持流式输出 (通常默认支持)
    llm = get_llm(temperature=0.7)
except ValueError as e:
    print(f"提示: {e}")
    print("在未配置 API Key 的情况下，此示例无法真正调用模型。")
    llm = None

# 3. 定义调用 LLM 的异步节点
async def call_llm_node(state: MessageState) -> dict:
    print("\n[Node: call_llm_node] 正在向 LLM 发起请求...")
    # 使用 ainvoke 异步调用模型
    response = await llm.ainvoke(state["prompt"])
    return {"reply": response.content}

# 4. 构造并编译图
workflow = StateGraph(MessageState)
workflow.add_node("chat_model", call_llm_node)
workflow.add_edge(START, "chat_model")
workflow.add_edge("chat_model", END)
app = workflow.compile()

# 5. 使用 astream_events 流式打印 Token
async def main():
    if llm is None:
        print("请在 `.env` 中填写正确的 API KEY 后运行本脚本以进行流式 Token 测试。")
        return

    prompt_input = {"prompt": "请给我写一首关于人工智能与有状态图（LangGraph）的短诗，40字左右。"}
    print(f"提示词: {prompt_input['prompt']}\n")
    print("--- 开始接收实时 Token 流 (打字机效果) ---")

    # 使用 astream_events 方法，它可以捕获图内部所有子步骤（包括 LLM 内部的 Token 吐出事件）
    # version="v2" 是当前推荐的事件流协议版本
    async for event in app.astream_events(prompt_input, version="v2"):
        kind = event["event"]
        
        # 筛选：仅监听聊天模型输出流的事件
        if kind == "on_chat_model_stream":
            # 获取当前吐出的增量 Token
            chunk = event["data"]["chunk"]
            # 实时打印 Token，不换行，且强制刷新缓存
            print(chunk.content, end="", flush=True)

    print("\n\n--- 流式结束 ---")

if __name__ == "__main__":
    # 异步启动
    asyncio.run(main())
