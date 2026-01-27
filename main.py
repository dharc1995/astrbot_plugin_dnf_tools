import os
import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.model import MessageChain
from astrbot.api.model.base import Image
# 引入业务逻辑
from .config_manager import ConfigManager
from .lucky_logic import LuckyLogic
from .reply_logic import ReplyLogic

@register("dnf_tools", "Gemini", "DNF工具箱-解耦带注释版", "2.0.0")
class DNFToolsPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        p_path = os.path.dirname(__file__)
        # 初始化各个组件
        self.cfg_mgr = ConfigManager(p_path)
        self.lucky_logic = LuckyLogic(self.cfg_mgr)
        self.reply_logic = ReplyLogic(self.cfg_mgr, p_path)

    @filter.command("幸运频道")
    async def lucky_channel(self, event: AstrMessageEvent):
        """响应幸运频道指令"""
        res, t_range = self.lucky_logic.get_lucky_result(event.get_sender_id())
        if res: 
            yield event.plain_result(f"{event.get_sender_name()}, 今天的幸运频道是 {res}！\n有效时间：{t_range}")

    @filter.command("添加回复")
    async def add_reply(self, event: AstrMessageEvent):
        """管理指令：添加自定义回复"""
        # 权限判定：仅限管理员
        if not event.event.message_obj.sender.role.name in ["ADMIN", "OWNER"]: return
        
        # 解析指令中的关键词
        parts = event.get_plain_text().replace("添加回复", "").strip().split(maxsplit=1)
        if not parts: return
        
        keyword = parts[0]
        # 查找消息链中是否存在图片
        img_node = next((n for n in event.get_messages() if isinstance(n, Image)), None)
        
        if img_node: # 如果有图，执行图片添加逻辑
            ok, res = self.reply_logic.add_reply(keyword, "image", "", url=img_node.url)
        elif len(parts) > 1: # 否则执行纯文本添加逻辑
            ok, res = self.reply_logic.add_reply(keyword, "text", parts[1])
        else: 
            return
        
        yield event.plain_result(f"添加{'成功' if ok else '失败'}: {res}")

    @filter.on_decorators([filter.event_message])
    async def handle_words(self, event: AstrMessageEvent):
        """全量消息处理器：处理关键词自动回复"""
        # 匹配回复内容
        r_type, content = self.reply_logic.match_reply(event.get_plain_text().strip())
        
        if r_type == "text": 
            yield event.plain_result(content)
        elif r_type == "image" and os.path.exists(content):
            # 构造图片消息链
            yield event.chain_result(MessageChain().chain([Image.fromFileSystem(content)]))