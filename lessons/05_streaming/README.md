# 阶段 5: 响应式流式传输 (Streaming)

在构建交互式应用（如 Chat 界面）时，长时间等待 Agent 给出完整回答会导致极差的用户体验。LangGraph 提供了业内最完备的流式输出支持。

---

## 核心概念

1. **`stream` API**:
   * 与普通的 `invoke` 阻塞等待结果不同，`stream(input, config, stream_mode="...")` 返回一个 Python 生成器（Generator），可以边执行边消费数据。
2. **Stream Modes (流式模式)**:
   * **`values`**: 每次有节点修改了 State，流式输出**整个完整的 State** 副本。适合需要跟踪状态全貌的场景。
   * **`updates`**: 每次节点执行完成，流式输出**被触发节点及其返回的局部更新增量**。例如 `{"node_name": {"key_to_update": "new_value"}}`。这是最常用、效率最高的追踪节点路径的方式。
   * **`debug`**: 输出极其详尽的调试日志，包括输入、输出、当前 checkpoint ID 等。
3. **LLM Token Streaming (大模型 Token 流)**:
   * 可以在节点执行过程中，流式实时返回大模型（如 GPT）正在吐出的 Token，用于在 UI 上实现酷炫的“打字机”实时输出。

---

## 关卡任务

### [任务 1: 状态流与增量更新流](file:///app/lessons/05_streaming/01_stream_values_and_updates.py)
* **目标**: 学习如何使用 `stream` 方法，并对比在 `values` 模式和 `updates` 模式下获取到的数据结构差异。
* **文件**: `01_stream_values_and_updates.py`

### [任务 2: 大模型实时 Token 流](file:///app/lessons/05_streaming/02_stream_llm_tokens.py)
* **目标**: 学习如何在 LangGraph 的 Node 中通过事件回调，实时监听并流式吐出大模型的每一个 Token。
* **文件**: `02_stream_llm_tokens.py`

---

## 运行方法 (Docker 内)
```bash
docker compose exec app python lessons/05_streaming/01_stream_values_and_updates.py
docker compose exec app python lessons/05_streaming/02_stream_llm_tokens.py
```
