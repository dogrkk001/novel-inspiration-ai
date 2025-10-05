# 小说灵感提取AI系统

一个智能化的小说创作灵感提取与分析系统，支持从多种格式的小说文本中自动提取主题、人物、世界观等创作元素。

## 🎯 项目目标

- 🤖 **智能提取**：使用大语言模型从小说文本中提取创作灵感
- 📚 **多格式支持**：支持 TXT、PDF、EPUB 等常见文本格式  
- 🔍 **智能检索**：基于向量数据库的相似度检索功能
- 💾 **数据管理**：结构化存储提取的灵感内容
- 🚀 **易于使用**：简洁的命令行和 Web 界面

## ⚙️ API Key 配置

**重要**: 使用前请先配置API key。本项目支持多种LLM服务商：

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

⚠️ **安全提醒**：
- 绝不要将包含真实API key的文件提交到版本控制
- `.env` 文件已包含在 `.gitignore` 中
- 定期轮换您的API key

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置API key (见上方说明)

# 3. 运行测试
python -m pytest tests/ -v

# 4. 使用MockLLM演示完整流程
python demo_pipeline.py --input data/sample_novel.txt --db demo.db --keyword "武功"
```

## 📝 许可证

MIT License