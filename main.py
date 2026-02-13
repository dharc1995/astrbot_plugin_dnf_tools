from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from typing import AsyncGenerator
import json
from .lucky_channel.lucky import Lucky_Channel


@register("dnftools", "114514", "DNF工具插件", "v0.3.4", "https://github.com/dharc1995/astrbot_plugin_dnf_tools")
class DNFPlugin(Star):
    """DNF工具插件，提供幸运频道查询功能"""
    
    def __init__(self, context: Context) -> None:
        """初始化插件
        
        Args:
            context: AstrBot插件上下文
        """
        super().__init__(context)
        self.lc = Lucky_Channel()  # 初始化 Lucky_Channel 类的实例

    @filter.command("幸运频道")
    async def lucky_channel(self, event: AstrMessageEvent) -> AsyncGenerator[MessageEventResult, None]:
        """查询今日幸运频道
        
        根据用户QQ号和当前日期计算今日的幸运频道，结果每日固定。
        
        Args:
            event: 消息事件对象
            
        Yields:
            包含查询结果的MessageEventResult
        """
        # 1. 获取用户信息
        user_name = event.get_sender_name()
        qq_number = event.get_sender_id()  # 获取发送者 QQ 号/唯一 ID
        
        # 2. 调用逻辑类获取结果
        try:
            result_text = self.lc.get_lucky_msg(user_name, qq_number)
            
            # 3. 返回结果
            yield event.plain_result(result_text)
            
        except FileNotFoundError as e:
            logger.error(f"配置文件未找到: {e}")
            yield event.plain_result("查询失败：配置文件不存在，请检查插件配置。")
        except json.JSONDecodeError as e:
            logger.error(f"配置文件格式错误: {e}")
            yield event.plain_result("查询失败：配置文件格式错误，请检查JSON格式。")
        except Exception as e:
            logger.error(f"幸运频道插件运行出错: {e}")
            yield event.plain_result("查询失败，请检查插件配置或联系管理员。")

    async def terminate(self) -> None:
        """插件终止时调用，用于清理资源
        
        当插件被卸载或停用时，AstrBot会调用此方法。
        目前暂无需要清理的资源，保留方法以备将来扩展。
        """
        logger.info("DNF工具插件正在终止...")
        # 可以在此处添加资源清理逻辑，如关闭数据库连接等
