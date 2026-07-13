import sys
import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. 定义一个简单的数字 State
class CounterState(TypedDict):
    value: int

# 节点：每次执行将 value 增加 10
def add_ten(state: CounterState) -> dict:
    current = state.get("value", 0)
    new_value = current + 10
    print(f"[Node Execution] value 增加 10: {current} -> {new_value}")
    return {"value": new_value}

# 2. 构造并编译图
workflow = StateGraph(CounterState)
workflow.add_node("add_ten", add_ten)
workflow.add_edge(START, "add_ten")
workflow.add_edge("add_ten", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    print("--- 启动时间旅行 (Time Travel) 演示 ---")
    
    config = {"configurable": {"thread_id": "time_travel_demo"}}
    
    # 第一次运行
    print("\n--- 第一次运行 (初始值 0) ---")
    state = app.invoke({"value": 0}, config=config)
    
    # 第二次运行 (在上一轮状态基础上继续)
    print("\n--- 第二次运行 ---")
    state = app.invoke(None, config=config)
    
    # 第三次运行
    print("\n--- 第三次运行 ---")
    state = app.invoke(None, config=config)
    
    # 3. 检索所有的历史 Checkpoint
    print("\n--- 检索该 Thread 的历史状态快照 ---")
    history = list(app.get_state_history(config))
    
    print(f"总共记录了 {len(history)} 个历史状态点:")
    for i, historical_state in enumerate(history):
        checkpoint_id = historical_state.config["configurable"]["checkpoint_id"]
        val = historical_state.values.get("value")
        next_node = historical_state.next
        print(f"  快照 [{i}]: value = {val}, 下一步将触发的节点 = {next_node}, checkpoint_id = {checkpoint_id}")

    # 4. 执行时间旅行
    # 假设我们想回到“倒数第二次”运行的状态（即 value 为 20 的时候，也就是 history[1]）
    # 并从那一步重新分支出去，传入一个新的输入
    print("\n--- 穿越回倒数第二个 checkpoint (value = 20) 并分支出去 ---")
    
    # 获取倒数第二个状态的完整配置 (包含了特定的 checkpoint_id)
    target_history_point = history[1]
    historical_config = target_history_point.config
    
    # 从该历史状态重新触发运行
    # 注意：在 invoke 中我们传入 None 作为输入，它会直接从该 checkpoint 恢复执行
    forked_state = app.invoke(None, config=historical_config)
    
    print(f"时间旅行分支运行后的最终 value 值: {forked_state['value']} (期望是 30，即 20 + 10)")
