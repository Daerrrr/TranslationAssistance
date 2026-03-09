# -*- coding: utf-8 -*-
"""
翻译链构建（LangChain）
2. PromptTemplate：使用 ChatPromptTemplate 替代原有 string.Template；
3. TranslationChain：整合 PromptTemplate、ChatOpenAI 和输出解析器（StrOutputParser）。
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class TranslationChain:
    """
    翻译链类：整合 PromptTemplate、ChatOpenAI 和输出解析器。
    - PromptTemplate：ChatPromptTemplate（system + human 消息模板）
    - LLM：ChatOpenAI（由 ConfigManager 注入）
    - 输出解析器：StrOutputParser
    """

    def __init__(self, config_manager):
        self.llm = config_manager.llm
        self.prompt_template = self._create_prompt_template()
        self.chain = self._build_chain()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """使用 LangChain ChatPromptTemplate 替代原有 string.Template"""
        system_template = "你是一个专业的代码翻译专家，擅长将Java代码翻译成其他编程语言。"

        human_template = """请将以下Java代码翻译成{target_language}代码：


{java_code}

翻译要求：
1. 保持相同的功能逻辑和算法
2. 遵循{target_language}的最佳实践和编码规范
3. 添加必要的注释说明翻译考虑
4. 如果遇到Java特有特性（如synchronized、final等），提供{target_language}中的等价实现建议

请只输出翻译后的{target_language}代码，并在代码块前用注释说明翻译要点。"""

        return ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template)
        ])

    def _build_chain(self):
        """构建翻译链：ChatPromptTemplate | ChatOpenAI | StrOutputParser"""
        return (
            self.prompt_template
            | self.llm
            | StrOutputParser()
        )

    def translate(self, java_code: str, target_language: str = "Python") -> str:
        """
        翻译 Java 代码。
        :param java_code: Java 源代码
        :param target_language: 目标语言，默认 Python
        :return: 翻译后的代码字符串
        """
        try:
            return self.chain.invoke({
                "java_code": java_code,
                "target_language": target_language
            })
        except Exception as e:
            print(f"[错误] LangChain翻译失败：{e}")
            raise

    def batch_translate(self, code_list: list, target_language: str = "Python") -> list:
        """
        批量翻译 Java 代码。
        :param code_list: Java 代码列表
        :param target_language: 目标语言
        :return: 翻译结果列表
        """
        try:
            inputs = [
                {"java_code": code, "target_language": target_language}
                for code in code_list
            ]
            return self.chain.batch(inputs)
        except Exception as e:
            print(f"[错误] LangChain批量翻译失败：{e}")
            raise
