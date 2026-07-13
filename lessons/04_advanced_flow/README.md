# 阶段 4: 高级控制流 (高级图架构)

在设计更为复杂的 Agent 系统时，我们需要让节点能够并行执行以提高效率（例如同时调用多个 API 收集数据），或者将不同的子任务划分为单独的图以进行模块化组装。

---

## 核心概念

1. **Parallel Execution (并行执行)**:
   * 在 LangGraph 中，实现并行非常简单。如果两个不同的边同时指向不同的节点，例如从 `node_a` 出发有条边分别到 `node_b` 和 `node_c`。
   * 当它们执行完毕后汇聚到 `node_d` 时，LangGraph 会自动以并行方式（基于底层 asyncio 或线程池）执行 `node_b` 和 `node_c`。
2. **Subgraphs (子图)**:
   * 子图是指把一个独立的编译图（Compiled Graph）作为另一个父图中的一个节点。
   * 子图可以有独立的 State 定义，这样能极大简化单个图的逻辑，使之具备高内聚低耦合的特征。

---

## 关卡任务

### [任务 1: 并行分支与汇聚](file:///app/lessons/04_advanced_flow/01_parallel_execution.py)
* **目标**: 模拟一个工作流：接收一段原始文本后，同时进行“拼写错误纠正”和“关键字提取”，最后将这两个结果合并输出。
* **文件**: `01_parallel_execution.py`

### [任务 2: 模块化子图嵌套](file:///app/lessons/04_advanced_flow/02_subgraphs.py)
* **目标**: 学习如何定义一个“子图”处理特定任务（如数学计算），并将其嵌套嵌入到“主图”（聊天路由）中。
* **文件**: `02_subgraphs.py`

---

## 运行方法 (Docker 内)
```bash
docker compose exec app python lessons/04_advanced_flow/01_parallel_execution.py
docker compose exec app python lessons/04_advanced_flow/02_subgraphs.py
```
