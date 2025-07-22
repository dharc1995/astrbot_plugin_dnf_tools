from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

from .core import lucky_channel


@register("dnftools", "dharc1995", "dnftools", "1.0.0") 
class dnftools(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        message_str = event.message_str  # 获取消息的纯文本内容
        if message_str == "幸运频道":
            # 如果用户发送的消息是 "幸运频道"，则触发幸运频道指令
            user_name = event.get_sender_name()  # type: ignore # 获取用户的名称
            user_qq = event.get_sender_id()  # type: ignore # 获取用户的 QQ 号
            channel, channel_name = lucky_channel.lucky_channel(user_qq)  # 计算幸运频道
            yield event.plain_result(f"{user_name}, 你今天的幸运频道是 {channel}（{channel_name}）！")
    
    @filter.command("当前频道与大区列表")
    async def list_channels_list(self, event: AstrMessageEvent):
        '''
        列出当前的频道和大区对应的序号，用来对比本地序号是否与官方游戏更新保持一致。
        返回值为字符串格式，内容为频道与大区的对应列表，适合直接发送为纯文本消息。
        '''
        result = lucky_channel.list_all_channels_and_provinces()
        yield event.plain_result(result) # 发送一条纯文本消息
    
