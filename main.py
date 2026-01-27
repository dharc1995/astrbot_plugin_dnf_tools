import os
import re
import uuid
import requests
# 核心变化：直接从 event 导入 on
from astrbot.api.event import filter, AstrMessageEvent, on
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Image, Plain 

# 引入业务逻辑
from .config_manager import ConfigManager
from .lucky_logic import LuckyLogic
from .reply_logic import ReplyLogic

@register("dnf_tools", "Gemini", "DNF工具箱", "2.1.3")
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
        if not event.event.message_obj.sender.role.name in ["ADMIN", "OWNER"]: 
            return
        
        msg_text = event.get_plain_text().replace("添加回复", "").strip()
        parts = msg_text.split(maxsplit=1)
        if not parts: 
            yield event.plain_result("格式：添加回复 [关键词] [内容/图片]")
            return
        
        keyword = parts[0]
        
        # 获取图片节点
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

    # --- 修正后的监听写法 ---
    @on.message_created
    async def handle_words(self, event: AstrMessageEvent):
        """关键词自动回复监听：监听所有消息创建事件"""
        # 排除指令类消息，避免干扰
        full_text = event.get_plain_text().strip()
        if full_text.startswith("幸运频道") or full_text.startswith("添加回复") or full_text.startswith("/"):
            return
        
        r_type, content = self.reply_logic.match_reply(full_text)
        
        if r_type == "text": 
            yield event.plain_result(content)
        elif r_type == "image" and os.path.exists(content):
            yield event.chain_result([Image.fromFileSystem(content)])