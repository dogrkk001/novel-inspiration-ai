# 项目记忆系统 - Project Memory System

## 🧠 系统概述

项目记忆系统是为小说灵感AI项目开发的智能记忆管理工具，旨在帮助开发团队：

- 📝 **自动记录开发进度和关键决策**
- 🔍 **快速搜索和回顾历史信息**
- 🚀 **为新对话会话提供完整上下文**
- 💾 **持久化存储项目知识和经验**

## 🏗️ 系统架构

### 核心组件

1. **记忆模块** (`src/memory_module.py`)
   - SQLite数据库存储
   - 多种记忆类型支持
   - 搜索和筛选功能
   - 上下文导出和恢复

2. **CLI管理工具** (`src/memory_cli.py`)
   - 命令行接口
   - 快速记录功能
   - 数据导出和备份

3. **初始化脚本** (`init_memory_system.py`)
   - 系统初始化
   - 基础数据设置
   - 使用指南显示

### 记忆类型

- `PROJECT_INFO` - 项目基本信息
- `DEV_PROGRESS` - 开发进度记录
- `ARCHITECTURE` - 架构设计决策
- `BUG_FIXES` - 问题修复记录
- `FEATURE_IMPL` - 功能实现记录
- `CODE_REFACTOR` - 代码重构记录
- `TEST_RESULTS` - 测试结果记录
- `DEPLOYMENT` - 部署相关记录
- `DISCUSSION` - 技术讨论记录

### 优先级系统

- `CRITICAL` - 关键（项目核心信息）
- `HIGH` - 高优先级（重要功能和决策）
- `MEDIUM` - 中等优先级（常规开发记录）
- `LOW` - 低优先级（日常信息）

## 🚀 快速开始

### 1. 初始化系统

```bash
# 初始化记忆系统并记录基础信息
python init_memory_system.py
```

### 2. 基本使用

```bash
# 查看项目摘要
python src/memory_cli.py summary

# 快速记录开发进度
python src/memory_cli.py progress --title "完成功能X" --content "详细描述..."

# 快速记录BUG修复
python src/memory_cli.py bugfix --title "修复错误Y" --content "问题原因和解决方案"

# 搜索开发记录
python src/memory_cli.py search --type dev_progress --limit 10 --verbose

# 导出新对话上下文
python src/memory_cli.py export --output memories/session_context.json
```

## 💻 CLI命令参考

### 添加记忆

```bash
python src/memory_cli.py add \
  --type dev_progress \
  --title "功能标题" \
  --content "详细内容" \
  --tags "标签1,标签2" \
  --priority high \
  --files "file1.py,file2.js" \
  --context '{"key": "value"}'
```

### 搜索记忆

```bash
# 按类型搜索
python src/memory_cli.py search --type dev_progress --limit 5

# 按优先级搜索  
python src/memory_cli.py search --priority critical --verbose

# 按标签搜索
python src/memory_cli.py search --tags "UI,重构" --limit 10
```

### 快速记录

```bash
# 记录开发进度
python src/memory_cli.py progress \
  --title "实现用户认证" \
  --content "完成JWT认证系统" \
  --files "src/auth.py,src/middleware.py"

# 记录BUG修复
python src/memory_cli.py bugfix \
  --title "修复登录错误" \
  --content "解决会话过期问题" \
  --files "src/session.py"
```

### 数据管理

```bash
# 查看最近记忆
python src/memory_cli.py recent --days 7 --limit 20

# 备份数据
python src/memory_cli.py backup

# 导出上下文
python src/memory_cli.py export --output context.json
```

## 📁 文件结构

```
memories/
├── project_memory.db          # SQLite数据库
├── memory_backup.json         # JSON备份文件
├── memory_config.json         # 系统配置
├── session_context.json       # 导出的会话上下文
└── initial_session_context.json # 初始上下文

src/
├── memory_module.py           # 核心记忆模块
└── memory_cli.py             # CLI管理工具

init_memory_system.py         # 系统初始化脚本
demos/demo_memory_system.py   # 演示脚本
```

## 🔄 推荐工作流程

### 日常开发

1. **开发新功能时**
   ```bash
   python src/memory_cli.py progress --title "功能名称" --content "实现细节"
   ```

2. **修复BUG后**
   ```bash
   python src/memory_cli.py bugfix --title "问题描述" --content "解决方案"
   ```

3. **重要决策时**
   ```bash
   python src/memory_cli.py add --type architecture --title "设计决策" --content "原因和影响"
   ```

### 对话会话管理

1. **开始新对话前**
   ```bash
   python src/memory_cli.py export --output memories/current_session.json
   ```

2. **回顾项目状态**
   ```bash
   python src/memory_cli.py summary
   python src/memory_cli.py recent --days 14
   ```

3. **搜索相关信息**
   ```bash
   python src/memory_cli.py search --type dev_progress --tags "UI" --verbose
   ```

## 🎯 使用场景

### 1. 新对话会话恢复
- 导出完整项目上下文
- 快速了解项目现状
- 获取最新开发进度

### 2. 问题调试和回顾
- 搜索相关BUG修复记录
- 查看历史解决方案
- 分析问题模式

### 3. 代码审查和重构
- 回顾设计决策
- 查看功能实现历史
- 了解代码演进过程

### 4. 项目交接和文档
- 生成项目发展历程
- 导出关键决策记录
- 创建知识库文档

## ⚙️ 配置选项

配置文件: `memories/memory_config.json`

```json
{
  "max_records": 1000,
  "auto_backup": true,
  "retention_days": 365,
  "priority_weights": {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1
  }
}
```

## 🔧 高级功能

### 程序化使用

```python
from src.memory_module import ProjectMemory, MemoryType, Priority

# 创建记忆管理器
memory = ProjectMemory()

# 添加记忆
memory.add_memory(
    memory_type=MemoryType.DEV_PROGRESS,
    title="功能实现",
    content="详细描述",
    priority=Priority.HIGH
)

# 搜索记忆
results = memory.search_memories(
    memory_type=MemoryType.BUG_FIXES,
    limit=10
)

# 导出上下文
context = memory.export_context_for_new_session()
```

### 批量操作

```python
# 批量导入历史记录
records = [
    {"type": "dev_progress", "title": "...", "content": "..."},
    # ... 更多记录
]

for record in records:
    memory.add_memory(
        memory_type=MemoryType(record["type"]),
        title=record["title"],
        content=record["content"]
    )
```

## 🚨 注意事项

1. **数据备份**: 系统会自动备份到JSON文件，建议定期手动备份
2. **存储限制**: 默认保留1000条记录，可通过配置调整
3. **性能优化**: 大量数据时建议定期清理过期记录
4. **并发访问**: 系统不支持多进程并发写入

## 🤝 贡献指南

1. 确保所有新功能都有相应的测试
2. 遵循现有的代码风格和注释规范
3. 更新相关文档和使用示例
4. 提交前运行演示脚本验证功能

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🆘 故障排除

### 常见问题

1. **导入错误**: 确保在项目根目录运行脚本
2. **数据库锁定**: 避免多个进程同时操作数据库
3. **磁盘空间**: 定期清理过期记录和备份文件

### 诊断命令

```bash
# 检查系统状态
python src/memory_cli.py summary

# 验证数据完整性
python src/memory_cli.py backup

# 查看最近记录
python src/memory_cli.py recent --days 1 --verbose
```

---

📞 **联系方式**: 如有问题请通过项目Issues或邮件联系开发团队