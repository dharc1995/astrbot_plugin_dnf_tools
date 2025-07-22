import unittest
import time
from core import lucky_channel

class TestLuckyChannel(unittest.TestCase):
    def test_get_today_zero_timestamp(self):
        # Should return today's zero timestamp
        zero_ts = lucky_channel.get_today_zero_timestamp()
        t = time.localtime()
        expected = int(time.mktime((t.tm_year, t.tm_mon, t.tm_mday, 0, 0, 0, t.tm_wday, t.tm_yday, t.tm_isdst)))
        self.assertEqual(zero_ts, expected)

    def test_lucky_channel_consistency(self):
        # Same user_qq and same day should always return same result
        user_qq = "123456"
        result1 = lucky_channel.lucky_channel(user_qq)
        result2 = lucky_channel.lucky_channel(user_qq)
        self.assertEqual(result1, result2)
        self.assertIsInstance(result1, list)
        self.assertEqual(len(result1), 2)

    def test_lucky_channel_channel_name(self):
        # The channel name should be in channel_map or "未知频道"
        user_qq = "654321"
        ch, channel_name = lucky_channel.lucky_channel(user_qq)
        valid_names = set(lucky_channel.channel_map.values()) | {"未知频道"}
        self.assertIn(channel_name, valid_names)

    def test_list_all_channels_and_provinces(self):
        # Should contain all channels and provinces as strings
        output = lucky_channel.list_all_channels_and_provinces()
        for ch in lucky_channel.channel:
            self.assertIn(str(ch), output)
        for prov in lucky_channel.province:
            self.assertIn(str(prov), output)
        self.assertIn("频道列表:", output)
        self.assertIn("大区列表:", output)

if __name__ == "__main__":
    unittest.main()