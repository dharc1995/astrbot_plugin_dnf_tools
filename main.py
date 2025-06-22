from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import hashlib
import time
import random

province=[3,7,11,14,16,20,21,29,30,36,41,44,53,55,58,62]
channel=[20,67,21,22,23,24,25,26,27,28,29,30,31,32,68,69]
province_chanel_map = {
    20: "贝尔玛尔公国",
    67: "贝尔玛尔公国",
    21: "第七帝国",
    22: "魔界",
    23: "瓦哈伊特",
    24: "白海",
    25: "重力之泉",
    26: "重力之泉",
    27: "重力之泉",
    28: "重力之泉",
    29: "重力之泉",
    30: "重力之泉",
    31: "重力之泉",
    32: "重力之泉",
    68: "重力之泉",
    69: "重力之泉",
}
def lucky_channel(user_qq: str) -> str:
    """计算用户的幸运频道"""
    today_timestamp = int(time.mktime(time.localtime(time.time())[:3] + (0, 0, 0, 0, 0, -1)))  # 获取今天的时间戳
    random_seed = str(user_qq) + str(today_timestamp) # 使用 random_seed 作为种子，确保每次结果一致
    rng = random.Random(random_seed)
    province_index = rng.randrange(len(province))
    selected_province = province[province_index]
    channel_index = rng.randrange(len(channel))
    selected_chanel = channel[channel_index]
    ch = str(selected_province) + str(0) + str(selected_chanel)
    return ch
@register("dnftools", "dharc1995", "dnf幸运频道", "1.0.0")
class dnftools(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """处理所有消息事件"""
        # 这里可以添加通用的消息处理逻辑
        msg_obj=event.message_obj # 获取消息对象
        text=msg_obj.message_str or ""# 获取消息的纯文本内容

        if text=="幸运频道":
            # 如果用户发送的消息是 "幸运频道"，则触发幸运频道指令
            user_name=event.get_sender_name()  # 获取用户的名称
            user_qq=event.get_sender_id()  # 获取用户的 QQ 号
            channel = lucky_channel(user_qq)  # 计算幸运频道
            channel_name = province_chanel_map.get(int(channel[2:]), "未知频道")
            yield event.plain_result(f"{user_name}, 你今天的幸运频道是 {channel}（{channel_name}）！")
