## Human-in-the-loop 示例（HumanInTheLoopMiddleware）

这个示例会运行同一个问题两次：

- **无人干预**：正常让智能体调用工具 `add_numbers(a=12,b=8)`，得到 \(20\)
- **人工干预**：在工具调用前被 `HumanInTheLoopMiddleware` 中断，人为把参数改成 `b=80`，最终输出变成 \(92\)

### 运行方式（Windows）

从仓库根目录执行：

```bash
.\.venv\Scripts\python -m human_in_the_loop.main
```

