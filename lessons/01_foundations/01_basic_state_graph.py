from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义图的“状态 (State)”
# 状态是各个节点共享并修改的数据结构。
# 这里的 `messages` 键使用 Annotated 标记，并指定了 reducer 函数（这里是列表拼接 lambda x, y: x + y）。
# 每次节点返回 `{"messages": [...]}` 时，新列表会被追加到原有列表后，而不是覆盖它。
class SimpleState(TypedDict):
    messages: Annotated[list[str], lambda x, y: x + y]
    counter: int

# 2. 定义节点 (Nodes)
# 每个节点都是一个函数，输入是当前的 State，返回值是需要更新的 State 字典。
def node_one(state: SimpleState) -> dict:
    print(f"--- 触发 Node 1 ---")
    current_counter = state.get("counter", 0)
    return {
        "messages": [f"Node 1 发送了问候 (计数: {current_counter + 1})"],
        "counter": current_counter + 1  # 每次累加计数，更新策略为覆盖最新的值
    }

def node_two(state: SimpleState) -> dict:
    print(f"--- 触发 Node 2 ---")
    return {
        "messages": ["Node 2 完成了收尾工作！"]
    }

# 3. 定义条件路由函数 (Router for Conditional Edges)
# 条件路由函数返回下一步要去的目标节点名称（字符串）
def should_continue(state: SimpleState) -> str:
    # 如果 counter 达到 2，就走向 node_two，否则循环回 node_one
    if state.get("counter", 0) >= 2:
         print(">>> 路由判定: 计数达到上限，走向 Node 2")
         return "to_node_two"
    else:
         print(">>> 路由判定: 计数不足，返回 Node 1 进行循环")
         return "to_node_one"

# 4. 构建图结构
workflow = StateGraph(SimpleState)

# 添加节点到图中
workflow.add_node("node_one", node_one)
workflow.add_node("node_two", node_two)

# 配置流转关系
# 从 START 节点直接进入 node_one
workflow.add_edge(START, "node_one")

# 从 node_one 出发配置条件边
# 传入：起始节点、路由函数、路由映射表(返回值 -> 目标节点)
workflow.add_conditional_edges(
    "node_one",
    should_continue,
    {
        "to_node_one": "node_one",
        "to_node_two": "node_two"
    }
)

# 从 node_two 到结束
workflow.add_edge("node_two", END)

# 5. 编译图
# 编译后的 app 遵循 LangChain Runnable 协议，可以使用 invoke, stream 等方法
app = workflow.compile()

# 6. 执行图
if __name__ == "__main__":
    print("开始运行极简状态图实例...")
    
    # 初始状态
    initial_state = {
        "messages": ["初始启动消息"],
        "counter": 0
    }
    
    # 调用 invoke 运行
    result = app.invoke(initial_state)
    
    print("\n运行结束，最终状态 (State) 结果:")
    print(f"Counter: {result['counter']}")
    print("Messages:")
    for idx, msg in enumerate(result['messages']):
        print(f"  {idx + 1}. {msg}")
