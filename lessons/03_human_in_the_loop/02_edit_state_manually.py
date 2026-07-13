import sys
import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. 定义 SQL 自动执行 State
class SQLState(TypedDict):
    sql: str
    execution_result: str

# 2. 定义节点
def generate_code(state: SQLState) -> dict:
    # 模拟 Agent 写出了一个错误的 SQL（少写了 FROM）
    buggy_sql = "SELECT name, email users WHERE active = 1"
    print(f"[Agent Node] 生成了 SQL (有语法错误): '{buggy_sql}'")
    return {"sql": buggy_sql}

def execute_query(state: SQLState) -> dict:
    sql = state["sql"]
    print(f"[Database Node] 准备执行 SQL: '{sql}'")
    # 模拟数据库执行校验
    if "FROM" not in sql.upper():
        print("[Database Node] 错误！SQL 语法检查失败: 缺失 FROM 关键字！")
        return {"execution_result": "Error: Syntax Error"}
    else:
        print("[Database Node] 执行成功！返回 5 条活跃用户信息。")
        return {"execution_result": "Success: 5 active users returned"}

# 3. 构造并编译图，并设置在执行数据库节点前中断
workflow = StateGraph(SQLState)
workflow.add_node("generate_code", generate_code)
workflow.add_node("execute_query", execute_query)

workflow.add_edge(START, "generate_code")
workflow.add_edge("generate_code", "execute_query")
workflow.add_edge("execute_query", END)

memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["execute_query"]
)

if __name__ == "__main__":
    print("--- 启动人机协同修改状态测试 (State Editing) ---")
    
    config = {"configurable": {"thread_id": "sql_correction_session"}}
    
    # 1. 运行第一步
    print("\n步骤 1: 让 Agent 尝试生成 SQL...")
    state = app.invoke({"sql": "", "execution_result": ""}, config=config)
    
    # 2. 检查被挂起的状态
    current_state = app.get_state(config)
    print(f"\n当前图执行暂停。")
    print(f"生成的 SQL: '{current_state.values.get('sql')}'")
    print(f"即将运行的节点: {current_state.next}")
    
    # 3. 模拟人工介入，发现 SQL 写错了，在后台手工修改 State
    corrected_sql = "SELECT name, email FROM users WHERE active = 1"
    print(f"\n[主人修改] 纠正 SQL 语句为: '{corrected_sql}'")
    
    # 使用 update_state 直接干预图的状态
    # as_node 参数指定以哪个节点的身份进行修改，通常指派为生成该状态的节点
    app.update_state(
        config, 
        {"sql": corrected_sql}, 
        as_node="generate_code"
    )
    
    print("\n[状态已更新] 检查更新后的 SQL:")
    print(app.get_state(config).values)
    
    # 4. 恢复运行
    print("\n步骤 2: 恢复图的运行并执行 SQL...")
    final_state = app.invoke(None, config=config)
    
    print(f"\n最终执行结果: {final_state['execution_result']}")
