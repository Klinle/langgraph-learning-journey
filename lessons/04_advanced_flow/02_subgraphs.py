from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ==========================================
# 1. 定义子图 (Math Subgraph)
# ==========================================

# 子图的独立 State
class SubgraphState(TypedDict):
    number: int
    operation: str
    result: int

# 子图的计算节点
def perform_math(state: SubgraphState) -> dict:
    op = state["operation"]
    val = state["number"]
    print(f"  [子图执行] 正在处理运算: {op}({val})...")
    
    if op == "double":
        res = val * 2
    elif op == "square":
        res = val * val
    else:
        res = val
    return {"result": res}

# 构建并编译子图
sub_workflow = StateGraph(SubgraphState)
sub_workflow.add_node("perform_math", perform_math)
sub_workflow.add_edge(START, "perform_math")
sub_workflow.add_edge("perform_math", END)
math_subgraph = sub_workflow.compile()


# ==========================================
# 2. 定义主图 (Main Graph)
# ==========================================

# 主图的 State (它包含与子图同名的字段：number, operation, result)
# 当子图作为节点运行时，这些同名字段会自动在主图和子图之间进行双向同步。
class MainState(TypedDict):
    query: str
    number: int
    operation: str
    result: int
    output: str

# 主图的解析路由节点
def parse_query(state: MainState) -> dict:
    query = state["query"]
    print(f"[主图解析] 用户问题: '{query}'")
    
    # 模拟文本解析 (实际开发中这里会调用 LLM 结构化提取)
    if "双倍" in query or "乘2" in query:
        num = 12  # 模拟提取出数字 12
        op = "double"
    elif "平方" in query:
        num = 9   # 模拟提取出数字 9
        op = "square"
    else:
        num = 0
        op = "none"
        
    print(f"[主图解析] 提取结果: 数字 = {num}, 操作 = {op}")
    return {"number": num, "operation": op}

# 主图的响应格式化节点
def format_response(state: MainState) -> dict:
    print("[主图格式化] 正在生成最终答复...")
    # 从状态中读取子图写回的 'result'
    final_output = f"为您计算完毕：结果是 {state['result']}。"
    return {"output": final_output}

# 3. 构造主图架构
main_workflow = StateGraph(MainState)

# 注册主图节点
main_workflow.add_node("parse_query", parse_query)
# 核心：直接将编译好的【子图】作为主图的一个节点注册！
main_workflow.add_node("math_subgraph", math_subgraph)
main_workflow.add_node("format_response", format_response)

# 设置流转关系
main_workflow.add_edge(START, "parse_query")
main_workflow.add_edge("parse_query", "math_subgraph")  # 执行完解析后，自动将状态中的 number 和 operation 传入子图并触发子图
main_workflow.add_edge("math_subgraph", "format_response") # 子图执行结束后，自动把 result 同步回主图，并流转到格式化节点
main_workflow.add_edge("format_response", END)

# 编译主图
app = main_workflow.compile()

if __name__ == "__main__":
    print("--- 启动子图模块化嵌套测试 (Subgraphs) ---")
    
    # 测试输入 1
    input_data_1 = {"query": "请帮我算一下 12 的双倍是多少", "number": 0, "operation": "", "result": 0, "output": ""}
    res_1 = app.invoke(input_data_1)
    print(f"最终输出: {res_1['output']}\n")
    
    # 测试输入 2
    input_data_2 = {"query": "求一下数字 9 的平方是多少", "number": 0, "operation": "", "result": 0, "output": ""}
    res_2 = app.invoke(input_data_2)
    print(f"最终输出: {res_2['output']}")
