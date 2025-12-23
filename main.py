from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain
import copy
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
    @filter.command("goldprice")
    async def trigger_dnf(self, event: AstrMessageEvent):
        # 1. 获取指令字符串
        target_cmd = "/分析 https://www.yxdr.com/bijiaqi/dnf/youxibi/shanghai2"

        # 2. 构造一个模拟的事件
        # 既然 AiocqhttpMessageEvent 没有 clone，我们手动初始化一个
        # 注意：直接传递 event.message_obj 是最稳妥的，它包含了所有的 sender 权限信息
        new_event = AstrMessageEvent(
            message_obj=event.message_obj,
            vm=event.vm # 保持相同的虚拟机上下文
        )
        
        # 3. 覆盖消息内容为目标指令
        new_event.message_str = target_command
        new_event.message_obj.message = [Plain(target_command)]
        
        # 4. 寻找分发入口
        # 在新版 AstrBot 中，context 有一个核心引用通常叫 _context 或 engine
        # 最稳健的方法是使用 context.emit_event
        try:
            await self.context.emit_event(new_event)
        except Exception as e:
            # 如果 emit_event 也不行，尝试直接通过内部 handle_message
            # 部分版本中，核心实例可以通过这种方式访问
            await self.context.get_instance().handle_message(new_event.message_obj)
