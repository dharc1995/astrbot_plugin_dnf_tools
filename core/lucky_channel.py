import random
import datetime
from datetime import timezone


province=[3,7,11,14,16,20,21,29,30,36,41,44,53,55,58,62]
channel=[20,21,22,23,24,25,26,27,28,29,30,31,32]
channel_map = {
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
    68: "重力之泉",
    69: "重力之泉",
}
def get_dnf_date():
    """
    获取DNF游戏日期（基于北京时间6点刷新）
    如果北京时间 < 6:00，使用前一天；否则使用当天
    """
    # 获取当前UTC时间
    utc_now = datetime.datetime.now(timezone.utc)
    
    # 转换为北京时间（UTC+8）
    beijing_time = utc_now + datetime.timedelta(hours=8)
    
    # 如果北京时间在0:00-5:59之间，使用前一天的日期
    if beijing_time.hour < 6:
        dnf_date = (beijing_time - datetime.timedelta(days=1)).date()
    else:
        dnf_date = beijing_time.date()
    
    return dnf_date

def format_dnf_period(dnf_date):
    """
    格式化DNF时间段字符串
    格式: YYYY/M/D-6:00~YYYY/M/D-5:59
    """
    current_day = dnf_date
    next_day = current_day + datetime.timedelta(days=1)
    
    # 格式化日期部分（去掉前导零）
    current_str = f"{current_day.year}/{current_day.month}/{current_day.day}"
    next_str = f"{next_day.year}/{next_day.month}/{next_day.day}"
    
    return f"{current_str}-6:00~{next_str}-5:59"

def lucky_channel(user_qq: str):
     """
    根据字符种子和DNF日期作为随机种子，从全局数组中各抽取一个元素
    返回包含组合结果、频道名称和DNF时间段的数组
    
    参数:
    char_seed: 字符种子
    
    返回:
    [组合结果, 频道名称, DNF时间段字符串]
    """
    # 获取DNF游戏日期
    dnf_date = get_dnf_date()
    
    # 格式化时间段
    period_str = format_dnf_period(dnf_date)
    
    # 创建随机种子：字符 + DNF日期
    seed_str = f"{char_seed}{dnf_date}"
    seed_value = hash(seed_str)
    
    # 设置随机种子
    random.seed(seed_value)
    
    # 使用设置的随机种子来抽取元素
    province_index = random.randint(0, len(province) - 1)
    channel_index = random.randint(0, len(channel) - 1)
    
    province_element = province[province_index]
    channel_element = channel[channel_index]
    
    # 组合并在中间加上0
    combined_result = f"{province_element}0{channel_element}"
    
    # 查找频道名称
    channel_name = channel_map.get(channel_element, "未知频道")
    
    return [combined_result, channel_name, period_str]

def list_all_channels_and_provinces():
    """列出所有频道和对应的省份序号"""
    channel_list_str = "频道列表: " + "、 ".join([str(ch) for ch in channel])
    province_list_str = "大区列表: " + "、 ".join([str(prov) for prov in province])
    result = channel_list_str + "\n" + province_list_str
    return result