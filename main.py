import os
import re
import uuid
import requests
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Image, Plain 

# 引入业务逻辑
from .config_manager import ConfigManager
from .lucky_logic import LuckyLogic
from .reply_logic import ReplyLogic

@register("dnf_tools", "Gemini", "DNF工具箱", "2.1.2")
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
            yield event.plain_result(f"{event.get_sender_name()}, 今天的幸运频道是 {res}！\n有效时间：{t_range}")

    @filter.command("添加回复")
    async def add_reply(self, event: AstrMessageEvent):
        """管理指令：添加自定义回复"""
        # 权限判定
        if not event.event.message_obj.sender.role.name in ["ADMIN", "OWNER"]: 
            return
        
        # 解析指令
        msg_text = event.get_plain_text().replace("添加回复", "").strip()
        parts = msg_text.split(maxsplit=1)
        if not parts: 
            yield event.plain_result("格式：添加回复 [关键词] [内容/图片]")
            return
        
        keyword = parts[0]
        
        # 寻找图片节点
        img_node = None
        if event.message_obj and event.message_obj.message:
            for msg in event.message_obj.message:
                if isinstance(msg, Image):
                    img_node = msg
                    break
        
        if img_node: 
            ok, res = self.reply_logic.add_reply(keyword, "image", "", url=img_node.url)
        elif len(parts) > 1: 
            ok, res = self.reply_logic.add_reply(keyword, "text", parts[1])
        else: 
            yield event.plain_result("请提供回复内容或一张图片。")
            return
        
        yield event.plain_result(f"添加{'成功' if ok else '失败'}: {res}")

    # --- 关键修正点 ---
    @filter.on(filter.event_message)
    async def handle_words(self, event: AstrMessageEvent):
        """关键词自动回复监听"""
        # 逻辑：如果命中指令则不执行此监听逻辑，防止重复回复
        if event.get_plain_text().startswith("幸运频道") or event.get_plain_text().startswith("添加回复"):
            return
        
        r_type, content = self.reply_logic.match_reply(event.get_plain_text().strip())
        
        if r_type == "text": 
            yield event.plain_result(content)
        elif r_type == "image" and os.path.exists(content):
            yield event.chain_result([Image.fromFileSystem(content)])