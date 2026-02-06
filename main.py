from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger # 使用 astrbot 提供的 logger 接口
import json
from .lucky_channel.lucky import Lucky_Channel # 导入 lucky_channel 模块中的 LuckyChannel 类


@register("dnftools", "创P", "dnf工具", "0.3.1", "repo url")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.lc=Lucky_Channel() # 初始化 Lucky_Channel 类的实例

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("幸运频道")
    async def lucky_channel(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。非常建议填写。
        # 1. 获取用户信息
        user_name = event.get_sender_name()
        qq_number = event.get_sender_id() # 获取发送者 QQ 号/唯一 ID
        
        # 2. 调用逻辑类获取结果
        # 注意：这里的 get_lucky_msg 是同步函数，可以直接调用
        try:
            result_text = self.lc.get_lucky_msg(user_name, qq_number)
            
            # 3. 返回结果
            yield event.plain_result(result_text)
            
        except Exception as e:
            logger.error(f"幸运频道插件运行出错: {e}")
            yield event.plain_result("查询失败，请检查配置文件。")

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''