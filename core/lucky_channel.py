import random
import time


province=[3,7,11,14,16,20,21,29,30,36,41,44,53,55,58,62]
channel=[20,21,22,23,24,25,26,27,28,29,30,31,32]
province_chanel_map = {
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
def lucky_channel(user_qq: str) -> str:
    """计算用户的幸运频道"""
    today_timestamp = int(time.mktime(time.localtime(time.time())[:3] + (0, 0, 0, 0, 0, -1)))  # 获取今天的时间戳
    random_seed = str(user_qq) + str(today_timestamp) # 使用 random_seed 作为种子，确保每次结果一致
    rng = random.Random(random_seed)
    province_index = rng.randrange(len(province))
    selected_province = province[province_index]
    channel_index = rng.randrange(len(channel))
    selected_chanel = channel[channel_index]
    ch = str(selected_province) + str(0) + str(selected_chanel)
    return ch

def list_all_channels_and_provinces() -> list:
    """列出所有频道和对应的省份序号"""
    result = []
    result.append(channel) # type: ignore
    result.append(province) # type: ignore
    return result