# 小说灵感提取AI系统

一个智能化的小说创作灵感提取与分析系统，支持从多种格式的小说文本中自动提取主题、人物、世界观等创作元素。

[![GitHub Stars](https://img.shields.io/github/stars/dogrkk001/novel-inspiration-ai?style=social)](https://github.com/dogrkk001/novel-inspiration-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 项目目标

- 🤖 **智能提取**：使用大语言模型从小说文本中提取创作灵感
- 📚 **多格式支持**：支持 TXT、PDF、EPUB 等常见文本格式  
- 🔍 **智能检索**：基于向量数据库的相似度检索功能
- 💾 **数据管理**：结构化存储提取的灵感内容
- 🚀 **易于使用**：简洁的命令行和 Web 界面

## 🧩 核心功能

### 📖 文本处理
- 支持 TXT、PDF、EPUB 格式
- 智能章节识别和文本切分
- 中文分词和文本预处理

### 🎭 灵感提取
- 多模型支持：OpenAI GPT、Claude、Qwen、DeepSeek
- 提取主题、人物、世界观等创作元素
- 结构化输出，便于后续处理

### 💾 数据存储
- SQLite 数据库存储
- 支持批量操作
- 灵活的查询接口

### 🔍 智能检索
- 关键词检索
- 源文件筛选
- 日期范围查询

## ⚙️ API Key 安全配置

**⚠️ 重要**: 使用前请先配置API key。本项目采用安全的配置方式：

### 方式1：环境变量配置（推荐）

1. 复制配置模板：
   ```bash
   cp .env.template .env
   ```

2. 编辑 `.env` 文件，填入您的API key：
   ```bash
   OPENAI_API_KEY=sk-your-openai-key-here
   ANTHROPIC_API_KEY=sk-ant-your-claude-key-here
   QWEN_API_KEY=sk-your-qwen-key-here
   DEEPSEEK_API_KEY=sk-your-deepseek-key-here
   ```

### 方式2：配置文件
直接在 `llm_config.json` 中填入API key（**仅限本地开发**）

**📋 详细配置说明请参考 [API_KEY_CONFIG.md](API_KEY_CONFIG.md)**

### 🛡️ 安全提醒
- ✅ 绝不要将包含真实API key的文件提交到版本控制
- ✅ `.env` 文件已包含在 `.gitignore` 中
- ✅ 定期轮换您的API key
- ✅ 配置读取优先级：环境变量 > 配置文件

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/dogrkk001/novel-inspiration-ai.git
cd novel-inspiration-ai
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API Key
按照上述说明配置您的API密钥

### 4. 运行测试
```bash
python -m pytest tests/ -v
```

### 5. 体验完整流程
```bash
# 使用MockLLM演示（无需API key）
python demo_pipeline.py --input data/sample_novel.txt --db demo.db --keyword "武功"

# 使用真实LLM（需要配置API key）
python demo_pipeline.py --input data/sample_novel.txt --db demo.db --keyword "勇气" --use-llm
```

## 📖 使用示例

### 基本代码示例
```python
from src.input_module import InputModule
from src.extractor import InspirationExtractor, MockLLM
from src.database import save_batch
from src.search import search_inspirations

# 1. 读取和切分小说文件
input_module = InputModule()
result = input_module.process_file("data/sample_novel.txt")
text_chunks = result['chunks']

# 2. 提取灵感（使用MockLLM演示）
extractor = InspirationExtractor(llm=MockLLM())
inspirations = []

for chunk in text_chunks:
    inspiration_data = extractor.extract_inspiration(chunk['content'])
    db_data = {
        'source_file': "data/sample_novel.txt",
        'chapter': chunk.get('title', ''),
        'raw_text': chunk['content'][:500],
        'idea': inspiration_data['theme'],
        'tags': f"{inspiration_data['world_elements']}, {', '.join(inspiration_data['characters'])}"
    }
    inspirations.append(db_data)

# 3. 保存到数据库
saved_ids = save_batch(inspirations, "inspirations.db")
print(f"保存了 {len(saved_ids)} 条记录")

# 4. 检索灵感
results = search_inspirations("inspirations.db", "武功", limit=5)
for result in results:
    print(f"ID: {result['id']}, 创意: {result['idea']}")
```

### 命令行使用
```bash
# 完整流程演示
python demo_pipeline.py --input data/sample_novel.txt --db test.db --keyword "武功"

# 测试各个模块
python demo_extractor.py data/sample_novel.txt     # 测试提取模块
python demo_input_module.py data/sample_novel.txt  # 测试输入模块
python demo_search.py --db test.db --keyword "武功" # 测试搜索模块
```

## 🛠️ 开发指南

### 项目结构
```
novel-inspiration-ai/
├── src/                    # 核心代码模块
│   ├── input_module.py     # 文件读取和文本处理
│   ├── extractor.py        # 灵感提取和LLM集成
│   ├── database.py         # 数据存储管理
│   ├── search.py           # 检索功能
│   └── llm_manager.py      # LLM管理器
├── data/                   # 示例数据
├── tests/                  # 单元测试
├── .env.template          # 环境变量模板
├── requirements.txt       # 依赖包列表
└── demo_pipeline.py       # 完整流程演示
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_input_module.py -v

# 生成覆盖率报告
pytest --cov=src tests/
```

### 贡献指南
1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/新功能`
3. 提交更改：`git commit -am '添加新功能'`
4. 推送分支：`git push origin feature/新功能`
5. 提交 Pull Request

## 📊 项目状态

- ✅ **输入模块**：完整实现，支持多格式文件处理
- ✅ **灵感提取模块**：支持多种LLM，包含MockLLM用于测试
- ✅ **数据存储模块**：基于SQLite的结构化存储
- ✅ **检索模块**：支持关键词和高级查询
- ✅ **完整流程演示**：端到端演示脚本
- ✅ **测试套件**：完整的单元测试覆盖
- 🚧 **Web界面**：开发中

## 📋 支持的LLM

| 模型 | 状态 | 说明 |
|------|------|------|
| OpenAI GPT | ✅ | GPT-3.5/GPT-4 |
| Claude | ✅ | Claude-3 系列 |
| Qwen | ✅ | 通义千问 |
| DeepSeek | ✅ | DeepSeek Chat |
| MockLLM | ✅ | 测试用模拟模型 |

## 📝 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

## 📞 联系方式

- GitHub Issues: [提交问题](https://github.com/dogrkk001/novel-inspiration-ai/issues)
- GitHub Discussions: [参与讨论](https://github.com/dogrkk001/novel-inspiration-ai/discussions)

---

⭐ 如果这个项目对您有帮助，请给它一个星标！