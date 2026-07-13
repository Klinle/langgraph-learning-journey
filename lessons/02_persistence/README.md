# 阶段 2: 状态管理与持久化 (Persistence)

在实际的生产级 Agent 应用中，我们需要在多次交互中保留会话上下文（即记忆 Memory）。LangGraph 通过**检查点（Checkpointer）**机制提供了强大的持久化能力。

---

## 核心概念

1. **Checkpointer (检查点保存器)**:
   * 每当图执行一个步骤（通过节点）时，LangGraph 都会将当前的 State 快照保存到 Checkpointer 中。
   * 常见的实现有：`MemorySaver`（内存，适合开发测试）和基于数据库的 `SqliteSaver`、`PostgresSaver`（适合生产）。
2. **Thread (线程)**:
   * 线程是区分不同会话（Session）的唯一标识。
   * 运行时通过 `config = {"configurable": {"thread_id": "123"}}` 传入，LangGraph 会自动加载或保存该线程下的状态。
3. **Time Travel (时间旅行)**:
   * 由于状态是有版本记录的，我们可以读取某个历史版本的状态（Checkpoint）。
   * 并且可以从历史的某一步“分支”出新的状态并继续执行，实现错误回滚或调试。

---

## 关卡任务

### [任务 1: 内存持久化](file:///app/lessons/02_persistence/01_in_memory_checkpointer.py)
* **目标**: 学习如何使用内存版的 `MemorySaver` 实现一个多轮对话的简单 Agent。
* **文件**: `01_in_memory_checkpointer.py`

### [任务 2: SQLite 数据库持久化](file:///app/lessons/02_persistence/02_sqlite_checkpointer.py)
* **目标**: 学习如何使用 `SqliteSaver` 将状态写入本地 SQLite 文件，这样即使程序重启也能找回之前的对话记忆。
* **文件**: `02_sqlite_checkpointer.py`

### [任务 3: 时间旅行与状态回溯](file:///app/lessons/02_persistence/03_time_travel.py)
* **目标**: 学习如何检索某个 `thread_id` 下的历史 Checkpoint，并从历史版本重新分支出运行。
* **文件**: `03_time_travel.py`

---

## 运行方法 (Docker 内)
```bash
docker compose exec app python lessons/02_persistence/01_in_memory_checkpointer.py
docker compose exec app python lessons/02_persistence/02_sqlite_checkpointer.py
docker compose exec app python lessons/02_persistence/03_time_travel.py
```
