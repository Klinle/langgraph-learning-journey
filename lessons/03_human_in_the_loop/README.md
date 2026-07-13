# 阶段 3: 人机协同 (Human-in-the-loop)

在构建复杂的 Agent（如自动编码、API 写入、财务审批）时，我们不希望 Agent 完全失控。LangGraph 支持原生的人工干预，称为 **Human-in-the-loop**。

---

## 核心概念

1. **Interrupt (中断)**:
   * 可以在编译图时，设置在进入某个节点之前（`interrupt_before`）或之后（`interrupt_after`）暂停执行。
   * 当程序到达中断点时，图的执行会被挂起，并保存当前状态，返回给调用者。
2. **Resume (恢复)**:
   * 外部人工处理（比如批准、拒绝或填写表单）完毕后，可以通过 `app.invoke(None, config)` 传入一个空的输入（或者在 `resume` 参数中传入决策信息）来唤醒图，使其从中断的地方继续向下运行。
3. **State Editing (状态修改)**:
   * 在图暂停期间，人工可以通过 `app.update_state(config, values, as_node="xxx")` 直接修改图的当前状态值。
   * 这在纠正 Agent 的中间错误（比如 SQL 写错了，人工纠正后继续）时非常有用。

---

## 关卡任务

### [任务 1: 中断与审批恢复](file:///app/lessons/03_human_in_the_loop/01_interrupt_and_resume.py)
* **目标**: 模拟一个敏感的“转账系统”，在执行扣款前暂停，要求用户输入 “yes” 确认后才扣款，否则终止。
* **文件**: `01_interrupt_and_resume.py`

### [任务 2: 手工干预与修改状态](file:///app/lessons/03_human_in_the_loop/02_edit_state_manually.py)
* **目标**: 模拟 Agent 编写的代码有缺陷，人类开发者在中间环节直接“修改”状态中的代码，然后恢复运行。
* **文件**: `02_edit_state_manually.py`

---

## 运行方法 (Docker 内)
```bash
docker compose exec app python lessons/03_human_in_the_loop/01_interrupt_and_resume.py
docker compose exec app python lessons/03_human_in_the_loop/02_edit_state_manually.py
```
