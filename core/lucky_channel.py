import random
import time
import datetime


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
def get_today_zero_timestamp():
    """获取当天零点时间戳"""
    t = time.localtime()
    zero_time = time.struct_time((t.tm_year, t.tm_mon, t.tm_mday, 0, 0, 0, t.tm_wday, t.tm_yday, t.tm_isdst))
    return int(time.mktime(zero_time))

def lucky_channel(user_qq: str):
    """
    根据字符种子和调整后的日期作为随机种子，从全局数组中各抽取一个元素
    返回包含组合结果和频道名称的数组
    
    参数:
    char_seed: 字符种子
    
    返回:
    [组合结果, 频道名称]
    """
    # 获取当前UTC时间
    utc_now = datetime.datetime.utcnow()
    
    # 调整日期：北京时间6点 = UTC时间前一天的0点
    adjusted_time = utc_now - datetime.timedelta(hours=6)
    adjusted_date = adjusted_time.date()
    
    # 创建随机种子：字符 + 调整后的日期字符串
    seed_str = f"{user_qq}{adjusted_date}"
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
    
    return [combined_result, channel_name]

def list_all_channels_and_provinces():
    """列出所有频道和对应的省份序号"""
    channel_list_str = "频道列表: " + "、 ".join([str(ch) for ch in channel])
    province_list_str = "大区列表: " + "、 ".join([str(prov) for prov in province])
    result = channel_list_str + "\n" + province_list_str
    return result