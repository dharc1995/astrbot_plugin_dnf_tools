from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

from .core import lucky_channel
from .core import qixi_gacha

@register("dnftools", "dharc1995", "dnftools", "1.0.0")  # type: ignore
class dnftools(Star): # type: ignore
    def __init__(self, context: Context): # type: ignore
        super().__init__(context) # type: ignore
    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE) # type: ignore
    async def on_group_message(self, event: AstrMessageEvent): # type: ignore
        message_str = event.message_str  # type: ignore # 获取消息的纯文本内容
        if message_str == "幸运频道":
            # 如果用户发送的消息是 "幸运频道"，则触发幸运频道指令
            user_name = event.get_sender_name()  # type: ignore # 获取用户的名称
            user_qq = event.get_sender_id()  # type: ignore # 获取用户的 QQ 号
            channel, channel_name, date = lucky_channel.lucky_channel(user_qq)  # type: ignore # 计算幸运频道
            yield event.plain_result(f"{user_name}, 你今天（{date}）的幸运频道是 {channel}（{channel_name}）！") # type: ignore
    @filter.command("当前频道与大区列表") # type: ignore
    async def list_channels_list(self, event: AstrMessageEvent): # type: ignore
        '''
        列出当前的频道和大区对应的序号，用来对比本地序号是否与官方游戏更新保持一致。
        返回值为字符串格式，内容为频道与大区的对应列表，适合直接发送为纯文本消息。
        '''
        result = lucky_channel.list_all_channels_and_provinces()
        yield event.plain_result(result) # type: ignore # 发送一条纯文本消息
    @filter.command("咱俩试试") # type: ignore
    async def qixi_gacha(self, event: AstrMessageEvent): # type: ignore
        '''
        七夕限定卡池开催 
        编辑发送“咱俩试试？”
        即有机会获得限定ssr“好呀宝宝”
        '''
        qixi_config_data=qixi_gacha.config_data # type: ignore
        gacha=qixi_gacha.GachaSystem(qixi_config_data) # type: ignore
        user_name = event.get_sender_name()  # type: ignore # 获取用户的名称
        user_qq = event.get_sender_id()  # type: ignore # 获取用户的
        result = gacha.draw(user_qq) # type: ignore
        yield event.plain_result(f"{user_name}, 恭喜你抽到了 {result['item']} ！") # type: ignore
