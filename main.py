from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

from .core import lucky_channel


@register("dnftools", "dharc1995", "dnftools", "1.0.0") # type: ignore
class dnftools(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        message_str= event.message_str  # 获取消息的纯文本内容
        if message_str == "幸运频道":
            # 如果用户发送的消息是 "幸运频道"，则触发幸运频道指令
            user_name = event.get_sender_name()  # type: ignore # 获取用户的名称
            user_qq = event.get_sender_id()  # type: ignore # 获取用户的 QQ 号
            channel = lucky_channel.lucky_channel(user_qq)  # 计算幸运频道
            channel_name = lucky_channel.province_chanel_map.get(int(channel[2:]), "未知频道")
            yield event.plain_result(f"{user_name}, 你今天的幸运频道是 {channel}（{channel_name}）！")
    
    @filter.command("当前频道与大区列表")
    async def list_channels_list(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。非常建议填写。
        result = lucky_channel.list_all_channels_and_provinces()
        yield event.plain_result(result) # 发送一条纯文本消息
    
