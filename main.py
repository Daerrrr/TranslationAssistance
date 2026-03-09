# -*- coding: utf-8 -*-
"""
Java 代码智能翻译助手 - LangChain 升级版演示
主程序：演示从文件翻译与从文本翻译，保持 API 接口兼容。
"""
from pathlib import Path
import sys
import io

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 将项目根目录加入路径，便于直接运行 main.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

from java_code_translator import JavaCodeTranslator


def main():
    """主函数示例"""
    print("=" * 60)
    print("Java代码智能翻译助手 - LangChain升级版演示")
    print("=" * 60)

    translator = JavaCodeTranslator()

    # 示例1：从文件翻译
    print("\n[示例1] 从文件翻译")
    print("-" * 40)

    example_file = "data/input/Example.java"
    if Path(example_file).exists():
        result = translator.translate_from_file(example_file, "Python")
    else:
        print(f"[提示] 示例文件不存在：{example_file}")
        print("   将在 data/input/ 目录创建示例文件...")

        example_code = """
public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, World!");

        int sum = 0;
        for (int i = 1; i <= 10; i++) {
            sum += i;
        }
        System.out.println("Sum from 1 to 10 is: " + sum);
    }
}
"""
        input_dir = Path("data/input")
        input_dir.mkdir(parents=True, exist_ok=True)

        with open(example_file, "w", encoding="utf-8") as f:
            f.write(example_code)

        print(f"[OK] 已创建示例文件：{example_file}")

        result = translator.translate_from_file(example_file, "Python")

    # 示例2：从文本翻译
    print("\n[示例2] 从文本翻译")
    print("-" * 40)

    java_text = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int a, int b) {
        int result = 0;
        for (int i = 0; i < b; i++) {
            result = add(result, a);
        }
        return result;
    }
}
"""

    result = translator.translate_from_text(java_text, "Python")

    # 示例3：批量翻译（batch_translate）
    print("\n[示例3] 批量翻译 batch_translate")
    print("-" * 40)

    batch_codes = [
        "public class Hello { public static void main(String[] args) { System.out.println(\"Hi\"); } }",
        "public int add(int a, int b) { return a + b; }",
    ]
    batch_results = translator.translate_batch(batch_codes, "Python")
    if batch_results:
        print(f"[OK] 批量翻译完成，共 {len(batch_results)} 段")

    print("\n" + "=" * 60)
    print("LangChain升级版演示完成！")
    print("=" * 60)

    if result:
        print("[OK] LangChain集成验证通过")
        print("翻译结果保存在：data/output/")
        print("新特性：")
        print("   - 使用 PromptTemplate 管理提示词")
        print("   - 支持标准化错误处理")
        print("   - 易于扩展和定制")
    else:
        print("[FAIL] 升级验证失败，请检查配置和网络")


if __name__ == "__main__":
    main()
