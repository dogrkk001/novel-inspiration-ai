# API Key 配置说明

## 安全配置方式

本项目支持两种API key配置方式：

### 方式1：环境变量配置（推荐）

1. 复制 `.env.template` 文件为 `.env`：
   ```bash
   cp .env.template .env
   ```

2. 编辑 `.env` 文件，填入您的实际API key：
   ```
   OPENAI_API_KEY=sk-your-actual-openai-key
   ANTHROPIC_API_KEY=sk-ant-your-actual-claude-key
   QWEN_API_KEY=sk-your-actual-qwen-key
   DEEPSEEK_API_KEY=sk-your-actual-deepseek-key
   ```

### 方式2：配置文件（仅限本地开发）

在 `llm_config.json` 中直接填入API key（**仅限本地开发，切勿提交到版本控制**）：

```json
{
  "llm": {
    "openai": {
      "api_key": "sk-your-actual-openai-key"
    }
  }
}
```

## 安全注意事项

⚠️ **重要安全提醒**：
- 绝不要将API key提交到版本控制系统
- `.env` 文件已包含在 `.gitignore` 中
- 定期轮换您的API key
- 不要在日志中记录完整的API key

## 优先级

配置读取优先级：环境变量 > 配置文件

系统会优先使用环境变量中的配置，如果环境变量不存在，则使用配置文件中的值。