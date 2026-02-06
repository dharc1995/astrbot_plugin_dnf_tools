from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger # 使用 astrbot 提供的 logger 接口
from .lucky_channel.lucky import LuckyChannel # 导入 lucky_channel 模块中的 LuckyChannel 类

@register("dnftools", "创P", "dnf工具", "1.0.0", "repo url")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("幸运频道")
    async def lucky_channel(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。非常建议填写。
        user_name = event.get_sender_name()
        user_qq = event.get_sender_id()
        message_str = event.message_str # 获取消息的纯文本内容
        lc=LuckyChannel()
        logger.info("触发幸运频道指令!")
        yield event.plain_result(lc.get_lucky_message(user_name,user_qq)) # 发送一条纯文本消息

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''