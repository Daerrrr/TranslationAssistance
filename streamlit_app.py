# src/streamlit_app.py
import streamlit as st
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from java_code_translator import JavaCodeTranslator

# 页面配置
st.set_page_config(
    page_title="Java 代码翻译助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 初始化翻译器（使用缓存避免重复加载）
@st.cache_resource
def get_translator():
    """获取翻译器实例（全局单例）"""
    return JavaCodeTranslator()


# 应用标题
st.title("🤖 Java 代码智能翻译助手")
st.markdown("---")

# 创建两列布局
col_input, col_output = st.columns([0.5, 0.5], gap="large")

with col_input:
    st.subheader("📝 Java 代码输入")

    # 输入模式选择
    input_mode = st.radio(
        "输入方式",
        ["直接输入", "上传文件"],
        horizontal=True
    )

    # 根据模式显示不同输入组件
    java_code = ""

    if input_mode == "直接输入":
        java_code = st.text_area(
            "粘贴 Java 代码",
            height=300,
            placeholder="public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
            help="支持多行 Java 代码，会自动处理格式"
        )

        # 提供示例按钮
        if st.button("加载示例代码"):
            example_code = '''public class Calculator {
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
}'''
            st.session_state.example_code = example_code
            st.rerun()

        if 'example_code' in st.session_state:
            java_code = st.text_area(
                "粘贴 Java 代码",
                value=st.session_state.example_code,
                height=300
            )

    else:  # 文件上传模式
        uploaded_file = st.file_uploader(
            "选择 Java 文件",
            type=["java", "txt"],
            help="支持.java 或.txt 格式"
        )

        if uploaded_file is not None:
            java_code = uploaded_file.read().decode("utf-8")
            st.code(java_code[:500] + "..." if len(java_code) > 500 else java_code)

    # 翻译选项
    st.subheader("⚙️ 翻译配置")

    col_opt1, col_opt2 = st.columns(2)

    with col_opt1:
        target_lang = st.selectbox(
            "目标语言",
            ["Python", "JavaScript", "TypeScript", "C#", "Go"],
            index=0
        )

        add_comments = st.checkbox("添加解释注释", value=True)

    with col_opt2:
        optimize_code = st.checkbox("性能优化", value=False)
        generate_tests = st.checkbox("生成单元测试", value=False)

    # 翻译按钮
    if st.button("🚀 开始翻译", type="primary", use_container_width=True):
        if not java_code.strip():
            st.warning("请输入或上传 Java 代码")
        else:
            # 获取翻译器实例
            translator = get_translator()

            # 显示加载状态
            with st.spinner("正在翻译代码..."):
                # 执行翻译
                try:
                    result = translator.translate_from_text(
                        java_text=java_code,
                        target_language=target_lang
                    )

                    # 保存结果到会话状态
                    st.session_state.translation_result = result
                    st.session_state.source_code = java_code

                    st.rerun()

                except Exception as e:
                    st.error(f"翻译失败：{str(e)}")

with col_output:
    st.subheader("🐍 Python 翻译结果")

    # 显示历史结果或当前结果
    if 'translation_result' in st.session_state:
        result = st.session_state.translation_result

        # 结果显示区域
        st.code(result, language="python")

        # 操作按钮组
        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button("📋 复制代码", use_container_width=True):
                st.write("已复制到剪贴板")

        with col_btn2:
            # 避免 result 为 None 导致 Invalid binary data format；无内容时不提供下载
            if result:
                st.download_button(
                    label="💾 下载文件",
                    data=result,
                    file_name=f"translated_{target_lang.lower()}.py",
                    mime="text/x-python",
                    use_container_width=True
                )
            else:
                st.caption("无内容可下载")

        with col_btn3:
            if st.button("🔄 重新翻译", use_container_width=True):
                del st.session_state.translation_result
                st.rerun()

        # 代码对比（可选）
        with st.expander("📊 代码对比"):
            col_src, col_dst = st.columns(2)

            with col_src:
                st.caption("原始 Java 代码")
                st.code(st.session_state.source_code, language="java")

            with col_dst:
                st.caption(f"翻译为{target_lang}")
                st.code(result, language="python")

    else:
        st.info("👈 请在左侧输入 Java 代码并点击翻译按钮")

        # 显示示例翻译结果
        st.caption("示例预览：")
        example_result = '''# 计算器类 - 从 Java 翻译到 Python
class Calculator:
    def add(self, a: int, b: int) -> int:
        """加法运算，对应 Java 的 add 方法"""
        return a + b

    def multiply(self, a: int, b: int) -> int:
        """乘法运算，使用循环调用 add 方法实现"""
        result = 0
        for i in range(b):  # Python 的 range 从 0 开始，不包括 b
            result = self.add(result, a)
        return result

# 使用示例
if __name__ == "__main__":
    calc = Calculator()
    print(f"3 + 5 = {calc.add(3, 5)}")
    print(f"3 × 5 = {calc.multiply(3, 5)}")'''

        st.code(example_result, language="python")

# 侧边栏：设置和帮助
with st.sidebar:
    st.header("⚙️ 设置")

    # API 配置
    st.subheader("API 配置")
    
    # 检查是否配置了 secrets
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'deepseek' in st.secrets:
            st.success("✅ API 密钥已配置")
        else:
            st.warning("⚠️ 请在 Secrets 中配置 API 密钥")
    except:
        api_key = st.text_input(
            "DeepSeek API 密钥",
            type="password",
            help="请输入有效的 DeepSeek API 密钥"
        )

        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key

    # 翻译参数
    st.subheader("翻译参数")
    temperature = st.slider("温度", 0.0, 1.0, 0.1, 0.1)
    max_tokens = st.slider("最大 token 数", 100, 5000, 2000, 100)

    # 帮助信息
    st.markdown("---")
    st.subheader("❓ 使用帮助")

    with st.expander("如何获取 API 密钥"):
        st.write("1. 访问 https://platform.deepseek.com/")
        st.write("2. 注册并登录账户")
        st.write("3. 在 API 密钥页面生成新密钥")

    with st.expander("支持的功能"):
        st.write("✅ 单文件 Java 代码翻译")
        st.write("✅ 多种目标语言支持")
        st.write("✅ 代码注释生成")
        st.write("🔄 批量翻译（后续版本）")

    # 版本信息
    st.markdown("---")
    st.caption("版本 v1.0 · 基于 LangChain + DeepSeek")
    st.caption("Java 工程师 AI 转型学习计划 · Week3 Day1")

# 页脚信息
st.markdown("---")
st.caption("🔧 技术栈：Streamlit + LangChain + DeepSeek API")
st.caption("📚 学习目标：掌握 AI 应用 Web 界面快速开发")
