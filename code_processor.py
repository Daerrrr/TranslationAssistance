# -*- coding: utf-8 -*-
"""
代码处理器
负责从文件或文本读取Java代码，并进行基本验证。迁移后提示词由TranslationChain的PromptTemplate管理。
"""
from pathlib import Path


class CodeProcessor:
    """代码处理器：读取与验证Java代码"""

    def read_code_from_file(self, file_path: str) -> str:
        """
        从文件读取Java代码并验证。
        :param file_path: Java源文件路径
        :return: 文件内容字符串
        :raises FileNotFoundError: 文件不存在
        :raises ValueError: 文件为空或非Java文件
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在：{file_path}")

        if path.suffix.lower() != ".java":
            raise ValueError(f"仅支持 .java 文件，当前：{path.suffix}")

        content = path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"文件为空：{file_path}")

        return content

    def validate_java_code(self, code: str) -> bool:
        """
        对Java代码做简单格式校验（可选）。
        :param code: 代码字符串
        :return: 是否通过基本校验
        """
        if not code or not code.strip():
            return False
        return True
