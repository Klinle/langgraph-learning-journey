import time
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义 State
# 注意：对于需要合并的列表，我们使用了一个合并 reducer
class AnalysisState(TypedDict):
    input_text: str
    corrected_text: str
    keywords: Annotated[list[str], lambda x, y: x + y]
    final_output: str

# 2. 定义处理节点
def spell_checker(state: AnalysisState) -> dict:
    print("[Node: Spell Checker] 正在拼写纠错中...")
    # 模拟耗时操作，检验是否并行
    time.sleep(1)
    text = state["input_text"]
    # 假设把 "langgaph" 纠正为 "LangGraph"
    corrected = text.replace("langgaph", "LangGraph").replace("ai", "AI")
    print("[Node: Spell Checker] 拼写纠错完成。")
    return {"corrected_text": corrected}

def keyword_extractor(state: AnalysisState) -> dict:
    print("[Node: Keyword Extractor] 正在提取关键字...")
    time.sleep(1)
    # 简单提取关键字
    keywords = ["LangGraph", "AI开发", "多Agent"]
    print("[Node: Keyword Extractor] 关键字提取完成。")
    return {"keywords": keywords}

def synthesizer(state: AnalysisState) -> dict:
    print("\n[Node: Synthesizer] --- 汇聚节点被触发 ---")
    corrected = state["corrected_text"]
    keywords = state["keywords"]
    
    summary = (
        f"【最终处理报告】\n"
        f"1. 修正后的文本: {corrected}\n"
        f"2. 提取的核心关键字: {', '.join(keywords)}"
    )
    return {"final_output": summary}

# 3. 构造并行图架构 (Fan-out -> Fan-in)
workflow = StateGraph(AnalysisState)

workflow.add_node("spell_checker", spell_checker)
workflow.add_node("keyword_extractor", keyword_extractor)
workflow.add_node("synthesizer", synthesizer)

# 分流：从 START 同时指向两个并行分支节点
workflow.add_edge(START, "spell_checker")
workflow.add_edge(START, "keyword_extractor")

# 汇聚：将并行分支节点指向同一个合并节点
workflow.add_edge("spell_checker", "synthesizer")
workflow.add_edge("keyword_extractor", "synthesizer")

workflow.add_edge("synthesizer", END)

app = workflow.compile()

if __name__ == "__main__":
    print("--- 启动并行流控测试 (Parallel Execution) ---")
    start_time = time.time()
    
    initial_input = {
        "input_text": "在学习 langgaph 和 ai 的过程中，我深刻感受到了多Agent状态图的魅力。",
        "corrected_text": "",
        "keywords": [],
        "final_output": ""
    }
    
    result = app.invoke(initial_input)
    
    end_time = time.time()
    print(f"\n{result['final_output']}")
    print(f"\n[性能测试] 并行节点各自执行耗时 1s，总运行耗时: {end_time - start_time:.2f}s (若接近 1s 则代表并行成功)")
