# 主动结束回复

给 LLM 一个 `end_reply` 工具：当它已经把想说的都说完、没有更多内容要输出时，主动、干净地结束这一回合。

## 解决什么问题

AstrBot 的 agent 工具循环（`tool_loop_agent_runner`）里，模型在调用工具之后还会被请求「最后一轮」生成回复。如果这一轮模型交了**空回复**（无正文、无思考、无工具调用），provider 会把它判为「无输出」（`EmptyModelOutputError`），重试 3 次后报错并降级到 fallback provider —— 表现为「调用完工具就不回复 / 像挂了」。

`end_reply` 把「不再输出」从一次**故障**变成一次**主动、合法的结束**：模型调用它即可结束本回合，不会再触发空输出重试。

## 工作原理

`end_reply` 是一个无参 `@filter.llm_tool`，返回 `None`。工具执行器在拿到 `None` 后向 runner 传出 `resp is None`，runner 随即把 agent 状态切到 `DONE`，循环结束、不再请求下一轮。整个过程不调用 `stop_event()`，以免误伤模型在同一轮里已经写出的正文。

## 安装

把本仓库文件夹放进 AstrBot 的 `data/plugins/` 目录，在管理面板重载插件即可。无第三方依赖。

## 用法

在你的人设 / 系统提示词里告诉模型：**每一轮要么写出回复内容，要么调用 `end_reply` 结束，绝不要什么都不输出。** 例如：

```
说完了、没有别的要补充时，就调用 end_reply 干净收尾，别交空回复。
```

## License

MIT
