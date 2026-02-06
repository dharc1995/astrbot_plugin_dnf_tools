import json
import random
import os
from datetime import datetime, timedelta, timezone

class Lucky_Channel:
    def __init__(self, filename="config.json"):
        # 自动定位到当前 .py 文件所在的目录，确保 json 路径正确
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(base_path, filename)

    def _load_config(self):
        """内部方法：读取配置"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"找不到配置文件: {self.config_path}")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def update_config(self, json_string):
        """传入 JSON 字符串直接修改配置"""
        try:
            new_data = json.loads(json_string)
            # 校验必要字段
            required = ["province", "channel", "channel_map"]
            if not all(k in new_data for k in required):
                return "修改失败：输入的数据缺少必要字段 (province, channel, channel_map)"
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            return "修改成功！"
        except json.JSONDecodeError:
            return "修改失败：JSON 格式错误，请检查括号和引号。"
        except Exception as e:
            return f"修改异常: {str(e)}"

    def get_lucky_msg(self, username, qq_number):
        """获取幸运频道文案"""
        data = self._load_config()
        
        # 固定北京时间 (UTC+8)
        sha_tz = timezone(timedelta(hours=8))
        now = datetime.now(sha_tz)
        
        # 游戏 6:00 刷新逻辑
        # 如果当前北京时间小时数 < 6，则逻辑日期减去一天
        game_day = now - timedelta(days=1) if now.hour < 6 else now
        
        # 构造日期字符串 (2026/1/22 这种格式)
        start_str = f"{game_day.year}/{game_day.month}/{game_day.day}"
        end_day = game_day + timedelta(days=1)
        end_str = f"{end_day.year}/{end_day.month}/{end_day.day}"
        
        time_range = f"{start_str}-6:00~{end_str}-5:59"

        # 随机种子：QQ号 + 游戏天 (确保当日结果固定)
        seed_str = f"{qq_number}_{game_day.strftime('%Y%m%d')}"
        rng = random.Random(seed_str)
        
        # 抽取结果
        aa = rng.choice(data["province"])
        bb = rng.choice(data["channel"])
        channel_name = data["channel_map"].get(str(bb), "未知区域")
        
        return f"{username}, 你今天（{time_range}）的幸运频道是 {aa}0{bb}（{channel_name}）！"

# --- 以下为测试代码 ---
# 只有直接运行这个 py 文件时才会执行下面的代码
if __name__ == "__main__":
    # 1. 初始化类
    lc = Lucky_Channel("config.json")

    # 2. 模拟一份初始化配置字符串（如果 config.json 不存在时可以手动创建）
    init_json = """
    {
        "province": [3, 7, 11, 14, 16, 20, 21, 29, 30, 36, 41, 44, 53, 55, 58, 62],
        "channel": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
        "channel_map": {
            "20": "贝尔玛尔公国", "21": "第七帝国", "22": "魔界", "23": "瓦哈伊特",
            "24": "白海", "25": "重力之泉", "26": "重力之泉", "27": "重力之泉",
            "28": "重力之泉", "29": "重力之泉", "30": "重力之泉", "31": "重力之泉", "32": "重力之泉"
        }
    }
    """

    print("=== 开始功能测试 ===")
    
    # 测试：写入/更新配置
    print(f"1. 测试更新配置: {lc.update_config(init_json)}")

    # 测试：查询幸运频道
    test_user = "测试玩家"
    test_qq = "12345678"
    result = lc.get_lucky_msg(test_user, test_qq)
    print(f"2. 测试查询结果:\n   {result}")

    # 测试：再次查询（验证结果是否一致，即“每日固定”）
    result_again = lc.get_lucky_msg(test_user, test_qq)
    is_same = result == result_again
    print(f"3. 验证同日重复查询结果是否固定: {'通过' if is_same else '失败'}")