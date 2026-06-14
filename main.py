from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star


class EndReplyPlugin(Star):
    """给 LLM 一个「我说完了」工具：在没有更多内容要输出时主动、干净地结束本回合。

    背景：AstrBot 的 agent 工具循环里，如果模型在调用工具之后那一轮交了空回复
    （无正文、无思考、无工具调用），provider 会判为「无输出」并重试 3 次、最终报错降级。
    本插件提供 end_reply 工具——它返回 None，触发 runner 的 `resp is None` 分支
    （AgentState.DONE），让模型把「不再输出」变成一次主动、合法的结束，而不是故障。
    """

    def __init__(self, context: Context):
        super().__init__(context)

    @filter.llm_tool(name="end_reply")
    async def end_reply(self, event: AstrMessageEvent):
        """当你这一轮已经把想说的都表达完、没有更多内容要输出时，调用本工具干净地结束本回合。
        用它来代替「交一条空回复」——空回复会被系统判为无输出、反复重试并最终报错降级。
        注意：如果你还有话要说，就直接正常写出来，不要调用本工具。
        """
        # 返回 None → 工具执行器 yield None → agent 循环转入 DONE，不再请求「最后一轮」。
        # 不调用 stop_event()，以免误伤同一轮里模型已写出的正文。
        return None
