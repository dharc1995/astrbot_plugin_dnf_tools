import random
from datetime import datetime, timedelta

class LuckyLogic:
    def __init__(self, cfg_mgr):
        """
        :param cfg_mgr: 传入 ConfigManager 实例以读取配置
        """
        self.cfg_mgr = cfg_mgr

    def get_lucky_result(self, user_id):
        """计算当天的幸运频道"""
        cfg = self.cfg_mgr.load_config()
        all_options = []
        
        # 组合大区和频道数据
        for p in cfg.get("province", []):
            for c in cfg.get("channel", []):
                c_name = cfg.get("channel_map", {}).get(str(c), "未知区域")
                # 格式：大区不补0，频道补足2位（如 3020）
                all_options.append(f"{p}0{c:02d}（{c_name}）")
        
        if not all_options: return None, None
        
        # 判定逻辑日期：清晨 6:00 为界限
        now = datetime.now()
        logic_time = now - timedelta(days=1) if now.hour < 6 else now
        logic_date = logic_time.strftime("%Y/%m/%d")
        
        # 构造有效时间段的文本显示
        time_range = f"{logic_date}-6:00~{(logic_time + timedelta(days=1)).strftime('%Y/%m/%d')}-5:59"
        
        # 使用逻辑日期和用户唯一ID设置随机种子，确保结果在一天内对同一人固定
        random.seed(f"{logic_date}_{user_id}")
        return random.choice(all_options), time_range