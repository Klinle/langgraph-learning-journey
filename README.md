# LangGraph 关卡式系统化学习仓

欢迎主人来到您的 LangGraph 专属学习与实战仓库！

本项目根据 **LangGraph 官方最新开发文档** 的核心概念精心设计，采用“关卡闯关”式的目录结构进行演练，并深度整合了 **Docker 隔离开发环境**，旨在帮助主人从零基础迅速成长为能够独立架构生产级 Multi-Agent 系统的专家。

---

## 🐋 Docker 开发环境配置与运行指南

本仓已全面容器化，所有的 Python 脚本及其依赖库（包含大模型调用等）均在隔离容器中运行，无需污染宿主机环境。

### 1. 初始化环境变量
复制根目录下的 `.env.example` 并重命名为 `.env`：
* 在 `.env` 中填写主人真实的 `OPENAI_API_KEY`（如需代理，可配置 `OPENAI_API_BASE`）。
* **强烈建议配置 LangSmith 链路追踪参数**（即 `LANGCHAIN_API_KEY`），这是观察和调试 LangGraph 复杂图流转的绝佳利器。

### 2. 启动 Docker 容器
在项目根目录下，使用终端运行以下命令：
```bash
# 构建镜像并后台拉起容器
docker compose up -d --build
```
此时，容器将在后台挂起，同时会将当前项目文件夹实时挂载到容器的 `/app` 目录下。主人在 IDE（如 VSCode/PyCharm）中修改代码，容器内会立刻实时同步生效。

### 3. 如何在容器中运行各关卡代码
使用 `docker compose exec` 命令可以直接在容器内执行具体的 Python 代码。例如：
```bash
# 运行阶段 1 关卡 1 的示例代码
docker compose exec app python lessons/01_foundations/01_basic_state_graph.py
```

### 4. 关闭容器
学习完毕后，可通过以下命令停止容器：
```bash
docker compose down
```

---

## 🗺️ LangGraph 核心学习路线图

| 阶段 | 核心学习主题 | 掌握 of API / 概念 | 对应实践文件 (点击直达) | 进度 |
| :--- | :--- | :--- | :--- | :---: |
| **Stage 1<br>核心基础** | 状态图基础与 ReAct 架构 | `StateGraph`, `START`, `END`, `TypedDict`, `reducer`<br>条件路由：`add_conditional_edges`<br>内置 ReAct Agent 快速构建 | 1. [01_basic_state_graph.py](file:///d:/www.workforpy.com/LangGraph/lessons/01_foundations/01_basic_state_graph.py)<br>2. [02_react_agent_with_tool.py](file:///d:/www.workforpy.com/LangGraph/lessons/01_foundations/02_react_agent_with_tool.py) | [ ] |
| **Stage 2<br>状态管理** | 对话记忆与持久化数据库 | `MemorySaver` 内存持久化<br>`SqliteSaver` 磁盘数据库持久化<br>时间旅行：`get_state_history` / `checkpoint_id` | 1. [01_in_memory_checkpointer.py](file:///d:/www.workforpy.com/LangGraph/lessons/02_persistence/01_in_memory_checkpointer.py)<br>2. [02_sqlite_checkpointer.py](file:///d:/www.workforpy.com/LangGraph/lessons/02_persistence/02_sqlite_checkpointer.py)<br>3. [03_time_travel.py](file:///d:/www.workforpy.com/LangGraph/lessons/02_persistence/03_time_travel.py) | [ ] |
| **Stage 3<br>人机协同** | 审批流控制与状态纠偏 | 节点前/后中断：`interrupt_before` / `interrupt_after`<br>手动唤醒：`invoke(None, config)`<br>状态硬核干预：`update_state` | 1. [01_interrupt_and_resume.py](file:///d:/www.workforpy.com/LangGraph/lessons/03_human_in_the_loop/01_interrupt_and_resume.py)<br>2. [02_edit_state_manually.py](file:///d:/www.workforpy.com/LangGraph/lessons/03_human_in_the_loop/02_edit_state_manually.py) | [ ] |
| **Stage 4<br>高级控制流** | 模块化设计与并行处理 | `Parallel Fan-out / Fan-in` 并行扇出与汇聚<br>`Subgraphs` 父子图嵌套与其状态字段的双向映射 | 1. [01_parallel_execution.py](file:///d:/www.workforpy.com/LangGraph/lessons/04_advanced_flow/01_parallel_execution.py)<br>2. [02_subgraphs.py](file:///d:/www.workforpy.com/LangGraph/lessons/04_advanced_flow/02_subgraphs.py) | [ ] |
| **Stage 5<br>响应式流** | 交互体验升级 (Streaming) | 图级别流：`stream_mode="values"` 与 `"updates"`<br>模型级 Token 流：监听 `on_chat_model_stream` 事件 | 1. [01_stream_values_and_updates.py](file:///d:/www.workforpy.com/LangGraph/lessons/05_streaming/01_stream_values_and_updates.py)<br>2. [02_stream_llm_tokens.py](file:///d:/www.workforpy.com/LangGraph/lessons/05_streaming/02_stream_llm_tokens.py) | [ ] |
| **Stage 6<br>综合实战** | Multi-Agent 协同系统 | 复杂的监督者路由器 (Supervisor Router)<br>子图共享与同步<br>大项目架构封装与闭环交互 | 1. [projects/README.md](file:///d:/www.workforpy.com/LangGraph/projects/README.md) | [ ] |

---

## 🛠️ 脚手架辅助模块说明

为了降低编写代码时的低级冗余度，项目内置了基础的脚手架封装：
* **[config/llm.py](file:///d:/www.workforpy.com/LangGraph/config/llm.py)**: 提供了 `get_llm()` 工具函数。该函数会自动加载 `.env` 环境变量中的 `OPENAI_API_KEY` 和 `OPENAI_API_BASE`，统一生成配置合理的 ChatModel 实例。在各个关卡代码中，主人只需通过以下方式导入即可使用：
  ```python
  from config.llm import get_llm
  llm = get_llm(model_name="deepseek-v4-flash", temperature=0)
  ```

---

## 💡 进阶：如何利用 LangSmith 调试？

LangGraph 的本质是状态在复杂的图形结构中流转。因此，强烈推荐主人注册并使用 **[LangSmith](https://smith.langchain.com/)**：
1. 注册后，生成一个 `API_KEY`。
2. 填入 `.env` 中的 `LANGCHAIN_API_KEY` 变量。
3. 当主人在容器中运行任何代码时，运行的每一步状态转换、LLM 输入输出、工具调用细节都会以可视化图的形式实时上传到 LangSmith 仪表盘。这对于理解有状态 Agent 的内部运转极有助益！
