from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义简单的 State
class SimpleState(TypedDict):
    data: Annotated[list[str], lambda x, y: x + y]

# 2. 定义两个节点
def node_a(state: SimpleState) -> dict:
    print("\n   [执行] Node A")
    return {"data": ["A 产生了数据"]}

def node_b(state: SimpleState) -> dict:
    print("\n   [执行] Node B")
    return {"data": ["B 产生了数据"]}

# 3. 构造并编译图
workflow = StateGraph(SimpleState)
workflow.add_node("node_a", node_a)
workflow.add_node("node_b", node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

app = workflow.compile()

if __name__ == "__main__":
    initial_input = {"data": ["初始状态"]}

    print("=========================================")
    print(" 演示一: stream_mode='updates'")
    print(" 每次节点运行完，输出【该节点的增量更新字典】")
    print("=========================================")
    
    # updates 模式
    for event in app.stream(initial_input, stream_mode="updates"):
        print(f"收到更新事件 -> {event}")
        # 输出示例：{'node_a': {'data': ['A 产生了数据']}}
        
    print("\n=========================================")
    print(" 演示二: stream_mode='values'")
    print(" 每次状态发生改变时，输出【当前完整的 State】")
    print("=========================================")
    
    # values 模式
    for event in app.stream(initial_input, stream_mode="values"):
        print(f"收到状态事件 -> {event}")
        # 输出示例：{'data': ['初始状态', 'A 产生了数据', 'B 产生了数据']}
