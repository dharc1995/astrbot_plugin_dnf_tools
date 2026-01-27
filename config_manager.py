import json
import os

class ConfigManager:
    def __init__(self, plugin_path):
        """
        初始化配置管理器
        :param plugin_path: 插件根目录，用于定位配置文件
        """
        self.config_path = os.path.join(plugin_path, "config.json")
        # 如果配置文件不存在，则创建一个默认的
        if not os.path.exists(self.config_path):
            self.save_config(self.get_default_config())

    def get_default_config(self):
        """定义插件的初始默认数据结构"""
        return {
            "province": [3, 7, 11, 14, 16, 20, 21, 29, 30, 36, 41, 44, 53, 55, 58, 62],
            "channel": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
            "channel_map": {"20": "贝尔玛尔公国", "21": "第七帝国", "22": "魔界"},
            "custom_replies": {} # 自定义回复存储字典
        }

    def load_config(self):
        """从 JSON 文件加载配置"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except: 
            return self.get_default_config()

    def save_config(self, cfg):
        """将配置对象写回 JSON 文件"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)