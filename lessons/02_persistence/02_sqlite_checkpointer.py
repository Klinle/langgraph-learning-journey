import sys
import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. 定义 State 和简单的 Node
class SimpleChatState(TypedDict):
    messages: Annotated[list[dict], lambda x, y: x + y]

def chatbot(state: SimpleChatState) -> dict:
    last_msg = state["messages"][-1]["content"]
    # 简单的响应，拼接我们这是持久化模式
    reply = f"[SQLite Bot] 确认收到：'{last_msg}'。此对话已保存至磁盘 SQLite 数据库中。"
    return {"messages": [{"role": "assistant", "content": reply}]}

workflow = StateGraph(SimpleChatState)
workflow.add_node("chatbot", chatbot)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# 本地 SQLite 文件路径
DB_PATH = "learning_state.db"

if __name__ == "__main__":
    print(f"--- 启动 SQLite 磁盘持久化测试 ---")
    print(f"数据库文件: {DB_PATH}")
    
    # 2. 使用 SqliteSaver 连接本地数据库文件
    # 使用 context manager (with 语句) 可以保证连接被优雅地关闭
    with SqliteSaver.from_conn_string(DB_PATH) as memory:
        app = workflow.compile(checkpointer=memory)
        
        # 定义一个特定的 thread
        config = {"configurable": {"thread_id": "sqlite_user_session"}}
        
        print("\n第一步: 运行一条新消息...")
        input_data = {"messages": [{"role": "user", "content": "向 SQLite 发起对话。"}]}
        result = app.invoke(input_data, config=config)
        
        # 打印当前对话
        for msg in result["messages"]:
            print(f"  {msg['role']}: {msg['content']}")
            
        print("\n第二步: 再次运行，查看记忆是否拼接...")
        input_data_2 = {"messages": [{"role": "user", "content": "帮我看看你是否还记得前一句话？"}]}
        result_2 = app.invoke(input_data_2, config=config)
        
        print("\n完整对话历史:")
        for msg in result_2["messages"]:
            print(f"  {msg['role']}: {msg['content']}")
            
    print(f"\n[验证] 检查当前目录是否已生成数据库文件 '{DB_PATH}'...")
    if os.path.exists(DB_PATH):
        print("-> 验证成功！数据已持久化落盘。")
    else:
        print("-> 警告！未检测到数据库文件生成。")
