import os
import uuid
import requests

class ReplyLogic:
    def __init__(self, cfg_mgr, plugin_path):
        """
        :param cfg_mgr: 配置管理器实例
        :param plugin_path: 插件路径，用于存放图片文件夹
        """
        self.cfg_mgr = cfg_mgr
        self.img_dir = os.path.join(plugin_path, "img")
        # 确保图片存放文件夹存在
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

    def add_reply(self, keyword, r_type, content, url=None):
        """
        添加回复逻辑
        :param r_type: 'text' 或 'image'
        :param url: 图片的下载链接（仅在 type 为 image 时需要）
        """
        cfg = self.cfg_mgr.load_config()
        
        if r_type == "image" and url:
            # 自动生成随机文件名防止冲突
            file_name = f"{uuid.uuid4().hex}.png"
            path = os.path.join(self.img_dir, file_name)
            # 下载图片
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(path, "wb") as f: f.write(r.content)
                content = file_name # 数据库中只记录文件名，不记全路径
            else: 
                return False, "图片下载失败"
            
        # 更新配置字典
        cfg.setdefault("custom_replies", {})[keyword] = {"type": r_type, "content": content}
        self.cfg_mgr.save_config(cfg)
        return True, content

    def match_reply(self, message):
        """检查输入的消息是否命中了关键词库"""
        cfg = self.cfg_mgr.load_config()
        reply = cfg.get("custom_replies", {}).get(message)
        if not reply: return None, None
        
        if reply["type"] == "image":
            # 返回图片的绝对路径供 AstrBot 发送
            return "image", os.path.join(self.img_dir, reply["content"])
        return "text", reply["content"]