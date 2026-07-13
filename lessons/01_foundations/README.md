# 阶段 1: LangGraph 核心基础

欢迎来到 LangGraph 学习的第一阶段。在这一关中，我们将掌握 LangGraph 最基本的概念：图、状态、节点和边。

---

## 核心概念

1. **State (状态)**:
   * LangGraph 的核心是一个“状态机”。状态决定了图在运行期间流转的数据结构。
   * 通常定义为一个 Python `TypedDict` 或 Pydantic 模型的子类。
2. **Nodes (节点)**:
   * 节点是图中的执行单元。每个节点通常是一个 Python 函数（可以是同步的也可以是异步的）。
   * 节点的输入是当前图的 `State`，返回值是一个**包含要更新 of State 键值对的字典**。
3. **Edges (边)**:
   * 边定义了节点之间的流转关系。
   * **普通边 (Normal Edges)**: `graph.add_edge("node_a", "node_b")`，表示执行完 `node_a` 后无条件进入 `node_b`。
   * **条件边 (Conditional Edges)**: 根据路由函数的计算结果决定下一步走向哪一个节点。
4. **编译与运行 (Compile & Run)**:
   * 图定义完成后，必须调用 `graph.compile()` 将其编译为可运行的 `Runnable` 实例。
   * 运行编译后的图通常使用 `invoke()`、`stream()` 等方法。

---

## 关卡任务

### [任务 1: 极简状态图](file:///app/lessons/01_foundations/01_basic_state_graph.py)
* **目标**: 学习如何定义一个包含简单文本列表的 `State`，并通过两个节点对其进行修改和加工。
* **文件**: `01_basic_state_graph.py`

### [任务 2: 使用内置工具的 ReAct Agent](file:///app/lessons/01_foundations/02_react_agent_with_tool.py)
* **目标**: 学习如何编写一个拥有数学计算工具（如乘法）的智能代理，并能够根据工具执行结果返回最终答案。
* **文件**: `02_react_agent_with_tool.py`

---

## 运行方法 (Docker 内)
在项目根目录启动容器后，可以通过以下命令运行本关的示例代码：
```bash
docker compose exec app python lessons/01_foundations/01_basic_state_graph.py
docker compose exec app python lessons/01_foundations/02_react_agent_with_tool.py
```
