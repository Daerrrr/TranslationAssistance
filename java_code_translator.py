# -*- coding: utf-8 -*-
"""
Java 代码翻译器主类（LangChain 集成）
4. 主类集成：使用新的 LangChain 组件替代原 TranslationAPI。
   - ConfigManager（含 LangChainConfig）-> 配置与 LLM
   - TranslationChain（PromptTemplate + ChatOpenAI + StrOutputParser）-> 翻译
   - CodeProcessor / ResultPresenter 保持不变
"""
from pathlib import Path
from typing import Optional, List

from config_manager import ConfigManager
from code_processor import CodeProcessor
from translation_chain import TranslationChain
from result_presenter import ResultPresenter


class JavaCodeTranslator:
    """
    主类集成：使用 LangChain 组件替代原 TranslationAPI。
    依赖：ConfigManager（LangChainConfig + ChatOpenAI）、TranslationChain、CodeProcessor、ResultPresenter。
    """

    def __init__(self):
        print("初始化Java代码翻译器（LangChain版本）...")

        self.config = ConfigManager()
        self.processor = CodeProcessor()
        self.translation_chain = TranslationChain(self.config)  # 替代原 TranslationAPI
        self.presenter = ResultPresenter()

        print("初始化完成")

    def translate_from_file(
        self,
        file_path: str,
        target_language: str = "Python"
    ) -> Optional[str]:
        """
        从文件翻译 Java 代码（保持接口不变）。
        :param file_path: Java 文件路径
        :param target_language: 目标语言，默认 Python
        :return: 翻译后的代码，失败返回 None
        """
        try:
            java_code = self.processor.read_code_from_file(file_path)
            if not self.processor.validate_java_code(java_code):
                print("[错误] 代码校验未通过")
                return None

            translated_code = self.translation_chain.translate(
                java_code, target_language
            )

            self.presenter.display_result(
                java_code, translated_code, target_language
            )

            output_filename = (
                f"{Path(file_path).stem}_{target_language.lower()}.txt"
            )
            self.presenter.save_result(
                java_code,
                translated_code,
                target_language,
                output_filename
            )

            return translated_code

        except Exception as e:
            print(f"[错误] 翻译过程失败：{e}")
            return None

    def translate_from_text(
        self,
        java_text: str,
        target_language: str = "Python"
    ) -> Optional[str]:
        """
        从文本翻译 Java 代码（保持接口不变）。
        :param java_text: Java 源代码字符串
        :param target_language: 目标语言，默认 Python
        :return: 翻译后的代码，失败返回 None
        """
        try:
            if not self.processor.validate_java_code(java_text):
                print("[错误] 代码校验未通过")
                return None

            translated_code = self.translation_chain.translate(
                java_text, target_language
            )

            self.presenter.display_result(
                java_text, translated_code, target_language
            )

            output_filename = f"text_{target_language.lower()}.txt"
            self.presenter.save_result(
                java_text,
                translated_code,
                target_language,
                output_filename
            )

            return translated_code

        except Exception as e:
            print(f"[错误] 翻译过程失败：{e}")
            return None

    def translate_batch(
        self,
        code_list: List[str],
        target_language: str = "Python"
    ) -> Optional[List[str]]:
        """
        批量翻译多段 Java 代码（调用 TranslationChain.batch_translate）。
        :param code_list: Java 源代码字符串列表
        :param target_language: 目标语言，默认 Python
        :return: 翻译结果列表，失败返回 None
        """
        try:
            if not code_list:
                print("[错误] 代码列表为空")
                return None
            for code in code_list:
                if not self.processor.validate_java_code(code):
                    print("[错误] 存在无效代码片段，请检查后重试")
                    return None

            results = self.translation_chain.batch_translate(
                code_list, target_language
            )

            for i, (java_code, translated_code) in enumerate(
                zip(code_list, results), start=1
            ):
                self.presenter.display_result(
                    java_code, translated_code, target_language
                )
                output_filename = f"batch_{i}_{target_language.lower()}.txt"
                self.presenter.save_result(
                    java_code,
                    translated_code,
                    target_language,
                    output_filename
                )

            return results
        except Exception as e:
            print(f"[错误] 批量翻译失败：{e}")
            return None
