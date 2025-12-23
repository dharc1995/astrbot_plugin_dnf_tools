from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain

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
            channel, channel_name,date = lucky_channel.lucky_channel(user_qq)  # 计算幸运频道
            yield event.plain_result(f"{user_name}, 你今天（{date}）的幸运频道是 {channel}（{channel_name}）！")
    @filter.command("当前频道与大区列表")
    async def list_channels_list(self, event: AstrMessageEvent): # type: ignore
        '''
        列出当前的频道和大区对应的序号，用来对比本地序号是否与官方游戏更新保持一致。
        返回值为字符串格式，内容为频道与大区的对应列表，适合直接发送为纯文本消息。
        '''
        result = lucky_channel.list_all_channels_and_provinces()
        yield event.plain_result(result) # 发送一条纯文本消息
    @filter.command("查金价")
    async def call_other(self, event: AstrMessageEvent):
        # 1. 获取指令管理器
        t_mgr = self.context.t_mgr
        
        # 2. 查找 dnftools 插件注册的指令名 (假设指令是 /分析)
        # 注意：这里填写的是注册时的指令名称，不带斜杠
        target_cmd_name = "分析" 
        handler = t_mgr.get_handler(target_cmd_name)
        
        if handler:
            # 3. 直接调用该函数
            # 传入当前的 event，如果目标函数需要参数，可以作为关键字参数传入
            # 例如 dnf_search(event, name="角色名")
            try:
                await handler.func(event, name="https://www.yxdr.com/bijiaqi/dnf/youxibi/shanghai2") 
            except Exception as e:
                await self.context.send_message(event, f"调用失败: {str(e)}")
        else:
            await self.context.send_message(event, f"未找到指令: {target_cmd_name}")
