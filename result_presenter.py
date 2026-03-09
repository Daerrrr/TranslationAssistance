# -*- coding: utf-8 -*-
"""
结果展示与保存
负责将翻译结果展示到控制台并保存到文件，接口与迁移前保持一致。
"""
from pathlib import Path


class ResultPresenter:
    """结果展示器：展示并保存翻译结果"""

    def __init__(self, output_dir: str = "data/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def display_result(
        self,
        java_code: str,
        translated_code: str,
        target_language: str
    ) -> None:
        """
        在控制台展示原文与译文。
        :param java_code: 原始 Java 代码
        :param translated_code: 翻译后的代码
        :param target_language: 目标语言
        """
        print("\n" + "=" * 60)
        print("[原始] Java 代码")
        print("=" * 60)
        print(java_code[:500] + ("..." if len(java_code) > 500 else ""))
        print("\n" + "=" * 60)
        print(f"[翻译结果] {target_language}")
        print("=" * 60)
        print(translated_code[:800] + ("..." if len(translated_code) > 800 else ""))
        print("=" * 60)

    def save_result(
        self,
        java_code: str,
        translated_code: str,
        target_language: str,
        output_filename: str
    ) -> str:
        """
        将原文与译文保存到文件。
        :param java_code: 原始 Java 代码
        :param translated_code: 翻译后的代码
        :param target_language: 目标语言
        :param output_filename: 输出文件名（如 example_python.txt）
        :return: 保存后的完整路径
        """
        out_path = self.output_dir / output_filename
        content = (
            f"# 原始 Java 代码\n\n{java_code}\n\n"
            f"# 翻译结果（{target_language}）\n\n{translated_code}"
        )
        out_path.write_text(content, encoding="utf-8")
        print(f"[OK] 结果已保存：{out_path}")
        return str(out_path)
