import json
import random
import datetime
import sqlite3
from typing import List, Dict

class GachaSystem:
    def __init__(self, config_file: str = None, config_data: List[Dict] = None): # type: ignore
        """
        初始化抽卡系统
        
        Args:
            config_file: 配置文件路径
            config_data: 直接传入配置数小先小据
        """
        if config_data:
            self.items = config_data # type: ignore
        elif config_file:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.items = json.load(f)
        else:
            raise ValueError("必须提供配置文件路径或配置数据")
        
        # 验证权重总和
        total_weight = sum(item['weight'] for item in self.items) # type: ignore
        if abs(total_weight - 100) > 0.01:  # 允许微小误差
            raise ValueError(f"权重总和应为100，当前为{total_weight}")
        
        # 初始化数据库
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect('gacha_records.db')
        self.cursor = self.conn.cursor()
        
        # 创建记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gacha_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                draw_time TIMESTAMP NOT NULL,
                label TEXT NOT NULL,
                weight REAL NOT NULL,
                tag TEXT,
                type TEXT
            )
        ''')
        self.conn.commit()
    
    def draw(self, user: str) -> Dict: # type: ignore
        """
        执行一次抽卡
        
        Args:
            user: 抽卡者名称
            
        Returns:
            抽到的物品信息
        """
        # 根据权重随机选择
        weights = [item['weight'] for item in self.items] # type: ignore
        selected_item = random.choices(self.items, weights=weights, k=1)[0] # type: ignore
        
        # 记录抽卡结果
        draw_time = datetime.datetime.now()
        self.cursor.execute('''
            INSERT INTO gacha_records (user, draw_time, label, weight, tag, type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user, draw_time, selected_item['label'], selected_item['weight'], 
              selected_item.get('tag'), selected_item.get('type'))) # type: ignore
        self.conn.commit()
        
        return {
            'user': user,
            'time': draw_time,
            'item': selected_item
        } # type: ignore
    
    def query_records(self, user: str = None, limit: int = 10) -> List[Dict]: # type: ignore
        """
        查询抽卡记录
        
        Args:
            user: 指定用户，None表示所有用户
            limit: 返回记录数量限制
            
        Returns:
            抽卡记录列表
        """
        if user:
            self.cursor.execute('''
                SELECT user, draw_time, label, weight, tag, type 
                FROM gacha_records 
                WHERE user = ? 
                ORDER BY draw_time DESC 
                LIMIT ?
            ''', (user, limit))
        else:
            self.cursor.execute('''
                SELECT user, draw_time, label, weight, tag, type 
                FROM gacha_records 
                ORDER BY draw_time DESC 
                LIMIT ?
            ''', (limit,))
        
        records = []
        for row in self.cursor.fetchall():
            records.append({ # type: ignore
                'user': row[0],
                'draw_time': row[1],
                'label': row[2],
                'weight': row[3],
                'tag': row[4],
                'type': row[5]
            })
        
        return records # type: ignore
    
    def get_user_stats(self, user: str) -> Dict: # type: ignore
        """
        获取用户抽卡统计
        
        Args:
            user: 用户名
            
        Returns:
            统计信息
        """
        # 总抽卡次数
        self.cursor.execute('SELECT COUNT(*) FROM gacha_records WHERE user = ?', (user,))
        total_draws = self.cursor.fetchone()[0]
        
        # 各稀有度统计
        self.cursor.execute('''
            SELECT tag, COUNT(*) 
            FROM gacha_records 
            WHERE user = ? 
            GROUP BY tag
        ''', (user,))
        rarity_stats = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # 特殊类型统计
        self.cursor.execute('''
            SELECT type, COUNT(*) 
            FROM gacha_records 
            WHERE user = ? AND type IS NOT NULL
            GROUP BY type
        ''', (user,))
        type_stats = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        return {
            'total_draws': total_draws,
            'rarity_stats': rarity_stats,
            'type_stats': type_stats
        } # type: ignore
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()
config_data = [ # type: ignore
        {"label": "滚你妈的", "weight": 10, "tag": "R"},
        {"label": "去你妈的", "weight": 10, "tag": "R"},
        {"label": "你也配？", "weight": 10, "tag": "R"},
        {"label": "傻逼二次元", "weight": 10, "tag": "R"},
        {"label": "癔症又犯了？", "weight": 10, "tag": "R"},
        {"label": "死男同真恶心", "weight": 5, "tag": "SR"},
        {"label": "现在是幻想时刻", "weight": 5, "tag": "SR"},
        {"label": "柚子厨滚出去", "weight": 5, "tag": "SR"},
        {"label": "这是最后通牒", "weight": 5, "tag": "SR"},
        {"label": "以后不要再和我扯上关系", "weight": 5, "tag": "SR"},
        {"label": "被拉黑+屏蔽", "weight": 5, "tag": "SR"},
        {"label": "小男娘", "weight": 5, "tag": "SR"},
        {"label": "发来一张可爱图片", "weight": 2.5, "tag": "SR", "type": "image"},
        {"label": "收到一条信息", "weight": 2.5, "tag": "SR", "type": "quote"},
        {"label": "下次再说吧", "weight": 2.5, "tag": "SR"},
        {"label": "你是个好人", "weight": 2.5, "tag": "SR"},
        {"label": "我一直把你当好朋友", "weight": 2.5, "tag": "SR"},
        {"label": "滚出去", "weight": 2.489, "tag": "R"},
        {"label": "好呀宝宝", "weight": 0.01, "tag": "SSR", "type": "ssr"},
        {"label": "其实我也喜欢你好久了", "weight": 0.001, "tag": "SSR", "type": "ssr"}
    ]
# 示例使用
if __name__ == "__main__":
    # 配置数据
    
    # 初始化抽卡系统
    gacha = GachaSystem(config_data=config_data)
    
    try:
        # 示例抽卡
        result = gacha.draw("测试用户") # type: ignore
        print(f"抽卡结果: {result['item']['label']} (稀有度: {result['item']['tag']})")
        
        # 查询记录
        records = gacha.query_records("测试用户", 5) # type: ignore
        print("\n最近5条记录:")
        for record in records: # type: ignore
            print(f"{record['draw_time']} - {record['label']} ({record['tag']})")
        
        # 获取统计
        stats = gacha.get_user_stats("测试用户") # type: ignore
        print(f"\n统计信息: {stats}")
        
    finally:
        gacha.close()
