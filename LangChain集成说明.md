# Java 代码翻译助手 - LangChain 集成说明

## 1. 架构对比

### 原架构（原生 OpenAI SDK）
- `TranslationAPI` 直接使用 OpenAI 客户端调用 DeepSeek
- 提示词使用 `string.Template` 或字符串拼接

### 新架构（LangChain 集成）
- **ConfigManager**：使用 `LangChainConfig`(Pydantic) + `ChatOpenAI` 管理配置与 LLM
- **CodeProcessor**：保持不变，负责读取与校验 Java 代码
- **TranslationChain**：使用 `ChatPromptTemplate` → `ChatOpenAI` → `StrOutputParser` 组成链
- **ResultPresenter**：保持不变，负责展示与保存结果

## 2. 核心重构点

| 项目       | 原实现           | LangChain 实现                    |
|------------|------------------|-----------------------------------|
| 配置       | 普通 dict/环境变量 | `LangChainConfig`(Pydantic) + `ChatOpenAI` |
| 提示词     | string.Template  | `ChatPromptTemplate.from_messages` |
| API 调用   | 直接 openai 调用 | `chain.invoke()` / `chain.batch()` |
| 输出解析   | 手动取 content   | `StrOutputParser()`               |

## 3. 依赖

```
openai>=1.0.0
langchain-openai>=0.1.0
langchain-core>=0.2.0
pydantic>=2.0.0
```

安装：`pip install -r requirements.txt`

## 4. 环境变量

- `DEEPSEEK_API_KEY`：DeepSeek API 密钥（必填，否则使用文档中的默认测试密钥）

## 5. 使用方式（向后兼容）

```python
from java_code_translator import JavaCodeTranslator

translator = JavaCodeTranslator()

# 从文件翻译
translator.translate_from_file("data/input/Example.java", "Python")

# 从文本翻译
translator.translate_from_text("public class A { }", "Python")
```

## 6. 验收对应

- 文件翻译、文本翻译接口不变，功能对等
- 使用 PromptTemplate 管理提示词，便于维护
- 移除原生 OpenAI 直接调用，统一走 LangChain Chain
- 错误在 TranslationChain 与 JavaCodeTranslator 中捕获并打印，便于排查
