import sys
import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. 定义 State
# 我们使用普通的 TypedDict 演示，简单拼接消息
class ChatState(TypedDict):
    messages: Annotated[list[dict], lambda x, y: x + y]

# 2. 定义聊天 Node
def chatbot(state: ChatState) -> dict:
    # 模拟简单的回复，将上一条用户消息转换为大写加上问候
    last_user_message = state["messages"][-1]["content"]
    bot_reply = f"[Bot] 我听到了: '{last_user_message}'。欢迎学习 LangGraph 持久化！"
    return {"messages": [{"role": "assistant", "content": bot_reply}]}

# 3. 构造并编译图
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# 核心：引入 MemorySaver 作为 checkpointer
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    print("--- 启动内存持久化测试 ---")
    
    # 线程 1
    config_1 = {"configurable": {"thread_id": "session_1"}}
    print("\n[Thread 1] 发送第一条消息...")
    input_1 = {"messages": [{"role": "user", "content": "你好，我是主人甲。"}]}
    res = app.invoke(input_1, config=config_1)
    print(f"Bot 回复: {res['messages'][-1]['content']}")
    
    print("\n[Thread 1] 发送第二条消息（测试记忆延续）...")
    input_2 = {"messages": [{"role": "user", "content": "刚刚我告诉你我是谁来着？"}]}
    res = app.invoke(input_2, config=config_1)
    # 打印所有的对话历史
    print("当前历史对话记录:")
    for msg in res["messages"]:
        print(f"  {msg['role']}: {msg['content']}")
        
    # 线程 2 (测试隔离性)
    config_2 = {"configurable": {"thread_id": "session_2"}}
    print("\n[Thread 2] 开启新线程会话...")
    input_3 = {"messages": [{"role": "user", "content": "你好，我是主人乙。"}]}
    res_2 = app.invoke(input_3, config=config_2)
    print("Thread 2 历史记录:")
    for msg in res_2["messages"]:
        print(f"  {msg['role']}: {msg['content']}")
