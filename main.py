from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import hashlib
import time
import random

province=[3,7,11,14,16,20,21,29,30,36,41,44,53,55,58,62]
channel=[20,21,22,23,24,25,26,27,28,29,30,31,32]
province_chanel_map = {
    20: "贝尔玛尔公国",
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
}
@register("dnftools", "dharc1995", "dnf幸运频道", "1.0.0")
class dnftools(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.commands={
            "幸运频道123456":self.luckychannel
        }

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("频道")
    async def luckychannel(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name() # 获取用户的名称
        user_qq = event.get_sender_id() # 获取用户的 QQ 号
        today_timestamp = int(time.mktime(time.localtime(time.time())[:3] + (0, 0, 0, 0, 0, -1)))#  获取今天的时间戳   
        random_seed=str(user_qq)+str(today_timestamp)
        # 使用 random_seed 作为种子，确保每次结果一致
        rng = random.Random(random_seed)
        province_index = rng.randrange(len(province))
        selected_province = province[province_index]
        channel_index = rng.randrange(len(channel))
        selected_chanel = channel[channel_index]
        ch=str(selected_province)+str(0)+str(selected_chanel)
        channel_name = province_chanel_map.get(selected_chanel, "未知频道")        
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"{user_name}, 你今天的幸运频道是 {ch}（{channel_name}）！") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
