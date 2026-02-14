# 更新日志

所有对DNF工具插件 (astrbot_plugin_dnf_tools) 的显著更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且此项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [v0.3.5] - 2026-02-15

### 新增
- 更新插件版本号至 v0.3.5

## [v0.3.4] - 2026-02-07

### 改进
- 重写README文档，提供更详细的使用说明和配置指南
- 为lucky.py添加完整的类型提示，提高代码可读性和可维护性
- 改进代码文档，为所有公共方法和类添加详细的文档字符串
- 优化项目结构说明

### 修复
- 修正插件注册信息中的作者字段格式
- 更新Lucky_Channel注册名称

## [v0.3.2] - 2026-02-07

### 改进
- 更新幸运频道指令逻辑，添加更完善的异常处理机制
- 增强错误处理，提供更友好的用户错误提示
- 改进配置文件读取和验证逻辑

### 修复
- 修复配置文件路径处理问题

## [v0.3.1] - 2026-02-07

### 新增
- 初始版本发布，实现基本幸运频道功能
- 支持根据用户QQ号和当前日期计算今日的幸运频道
- 提供每日固定结果，同一用户在同一天获得相同结果
- 支持北京时间(UTC+8)和DNF游戏6:00刷新规则
- 可配置的省份、频道和频道名称映射

### 功能
- `/幸运频道` 命令查询今日幸运频道
- 支持通过配置文件自定义省份、频道和频道名称映射
- 完整的错误处理和日志记录

## 早期版本

### v0.3.0 及之前
- 项目初始化和基础功能开发
- 添加查金价功能（后续版本中可能已移除或重构）
- 基础插件框架搭建

---

**注意**: 此更新日志从v0.3.1版本开始详细记录，早期版本信息基于git提交历史整理。

[Unreleased]: https://github.com/dharc1995/astrbot_plugin_dnf_tools/compare/v0.3.5...HEAD
[v0.3.5]: https://github.com/dharc1995/astrbot_plugin_dnf_tools/compare/v0.3.4...v0.3.5
[v0.3.4]: https://github.com/dharc1995/astrbot_plugin_dnf_tools/compare/v0.3.2...v0.3.4
[v0.3.2]: https://github.com/dharc1995/astrbot_plugin_dnf_tools/compare/v0.3.1...v0.3.2
[v0.3.1]: https://github.com/dharc1995/astrbot_plugin_dnf_tools/releases/tag/v0.3.1