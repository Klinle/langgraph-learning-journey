import sys
import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. 定义转账 State
class TransferState(TypedDict):
    amount: float
    user_confirmed: bool
    status: str

# 2. 定义节点
def prepare_transfer(state: TransferState) -> dict:
    print(f"[Node: prepare_transfer] 准备转账，金额: ￥{state['amount']}")
    return {"status": "pending_approval"}

def execute_transfer(state: TransferState) -> dict:
    # 模拟扣款节点
    print("[Node: execute_transfer] 正在执行资金扣划...")
    return {"status": "completed"}

# 3. 构造图并设置中断点
workflow = StateGraph(TransferState)
workflow.add_node("prepare_transfer", prepare_transfer)
workflow.add_node("execute_transfer", execute_transfer)

workflow.add_edge(START, "prepare_transfer")
workflow.add_edge("prepare_transfer", "execute_transfer")
workflow.add_edge("execute_transfer", END)

# 必须配合 checkpointer 才能使用 interrupt 功能
memory = MemorySaver()

# 在编译时，声明在执行 "execute_transfer" 节点前暂停中断
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["execute_transfer"]
)

if __name__ == "__main__":
    print("--- 启动人机协同审批测试 (Interrupt & Resume) ---")
    
    config = {"configurable": {"thread_id": "transfer_thread_1"}}
    
    # 首次发起运行
    print("\n步骤 1: 提交一笔转账申请 ￥5000.00...")
    initial_input = {"amount": 5000.00, "user_confirmed": False, "status": "initiated"}
    
    # 启动图的执行
    state = app.invoke(initial_input, config=config)
    
    # 检查当前图的状态
    current_state = app.get_state(config)
    print(f"\n当前图执行暂停。")
    print(f"当前图状态值: {current_state.values}")
    print(f"下一个将要执行的节点: {current_state.next}")
    
    # 4. 模拟人工介入决策
    user_input = input("\n[主人确认] 是否批准这笔 ￥5000.00 的转账？(请输入 yes/no): ").strip().lower()
    
    if user_input == "yes":
        print("\n步骤 2: 批准通过，恢复图的运行...")
        # 恢复运行时，我们通过 update_state 更新确认标记
        app.update_state(config, {"user_confirmed": True}, as_node="prepare_transfer")
        
        # 传入 None 并带有相同的 config，图会从上次挂起的地方（execute_transfer）继续执行
        final_state = app.invoke(None, config=config)
        print(f"\n转账流程已结束。最终状态: {final_state}")
    else:
        print("\n步骤 2: 拒绝转账，流程终止。")
