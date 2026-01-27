import os
import re
import uuid
import requests
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
# 核心：只从 components 导入图片等组件
from astrbot.api.message_components import Image, Plain 

# 引入业务逻辑
from .config_manager import ConfigManager
from .lucky_logic import LuckyLogic
from .reply_logic import ReplyLogic

@register("dnf_tools", "Gemini", "DNF工具箱", "2.1.1")
class DNFToolsPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        p_path = os.path.dirname(__file__)
        self.cfg_mgr = ConfigManager(p_path)
        self.lucky_logic = LuckyLogic(self.cfg_mgr)
        self.reply_logic = ReplyLogic(self.cfg_mgr, p_path)

    @filter.command("幸运频道")
    async def lucky_channel(self, event: AstrMessageEvent):
        """响应幸运频道指令"""
        res, t_range = self.lucky_logic.get_lucky_result(event.get_sender_id())
        if res: 
            # 直接返回字符串，AstrBot 会自动包装
            yield event.plain_result(f"{event.get_sender_name()}, 今天的幸运频道是 {res}！\n有效时间：{t_range}")

    @filter.command("添加回复")
    async def add_reply(self, event: AstrMessageEvent):
        """管理指令：添加自定义回复"""
        # 权限判定
        if not event.event.message_obj.sender.role.name in ["ADMIN", "OWNER"]: return
        
        # 解析指令
        parts = event.get_plain_text().replace("添加回复", "").strip().split(maxsplit=1)
        if not parts: return
        
        keyword = parts[0]
        
        # 适配 v4.12.4 的图片获取方式
        img_node = None
        if event.message_obj and event.message_obj.message:
            for msg in event.message_obj.message:
                if isinstance(msg, Image):
                    img_node = msg
                    break
        
        if img_node: # 添加图片回复
            ok, res = self.reply_logic.add_reply(keyword, "image", "", url=img_node.url)
        elif len(parts) > 1: # 添加文本回复
            ok, res = self.reply_logic.add_reply(keyword, "text", parts[1])
        else: 
            return
        
        yield event.plain_result(f"添加{'成功' if ok else '失败'}: {res}")

    @filter.on_decorators([filter.event_message])
    async def handle_words(self, event: AstrMessageEvent):
        """关键词自动回复监听"""
        # 忽略指令类消息，避免二次触发
        if event.get_plain_text().startswith("/"): return
        
        r_type, content = self.reply_logic.match_reply(event.get_plain_text().strip())
        
        if r_type == "text": 
            yield event.plain_result(content)
        elif r_type == "image" and os.path.exists(content):
            # 发送本地文件图片，直接 yield 列表即可
            yield event.chain_result([Image.fromFileSystem(content)])