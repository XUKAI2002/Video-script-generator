import streamlit as st
from utils import generate_script  # 从本地工具模块导入脚本生成函数
import time  # 添加重试机制需要

# 设置页面标题和图标
st.title("凯子视频脚本生成器")

# 侧边栏设置
with st.sidebar:
    # API密钥输入框（密码类型）
    deepseek_api_key = st.text_input("请输入API密钥：", type="password")

    st.markdown("提供相关视频文本生成")  # 说明文本

    # API连接测试按钮
    if st.button("测试API连接"):
        try:
            # 动态导入测试函数（避免未使用时加载）
            from utils import test_api_connection

            # 执行API连接测试
            if test_api_connection(deepseek_api_key):
                st.success("✅ API连接正常！")
            else:
                st.error("❌ API连接失败，请检查密钥")
        except Exception as e:
            st.error(f"连接测试失败: {str(e)}")  # 捕获并显示异常

# 主界面输入控件
# 视频主题输入框
subject = st.text_input("请输入视频的主题")
# 视频时长输入（带最小值限制和步长）
video_length = st.number_input("请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
# 创造力调节滑块
creativity = st.slider("请输入视频脚本的创造力（0.0-严谨，1.0-创意）",
                       min_value=0.0, max_value=1.0, value=0.5, step=0.1)
# 生成按钮
submit = st.button("生成脚本")

# 验证输入并处理提交
if submit:
    validation_errors = []  # 输入验证错误列表

    # 检查必填字段
    if not deepseek_api_key:
        validation_errors.append("请输入DeepSeek API密钥")
    if not subject:
        validation_errors.append("请输入视频主题")
    if not video_length >= 0.1:  # 确保时长有效
        validation_errors.append("视频时长需≥0.1分钟")

    # 显示所有验证错误
    if validation_errors:
        for error in validation_errors:
            st.error(error)
        st.stop()  # 终止脚本执行

    # 添加重试机制（最多3次尝试）
    max_retries = 3
    retry_delay = 5  # 重试间隔(秒)

    for attempt in range(max_retries):
        try:
            # 显示带重试进度的加载状态
            with st.spinner(f"AI创作中 (尝试 {attempt + 1}/{max_retries})..."):
                # 调用生成函数（参数来自用户输入）
                search_result, title, script = generate_script(
                    subject,
                    video_length,
                    creativity,
                    deepseek_api_key
                )

            # 成功生成后显示结果
            st.success("视频脚本生成成功！")
            # 显示标题
            st.subheader("标题：")
            st.write(title)
            # 显示脚本内容
            st.subheader("视频脚本：")
            st.write(script)

            # 添加下载功能
            st.download_button(
                label="下载脚本",
                data=f"标题: {title}\n\n脚本:\n{script}",  # 格式化文本内容
                file_name=f"{subject}_视频脚本.txt",  # 动态生成文件名
                mime="text/plain"  # MIME类型
            )

            break  # 成功则退出重试循环

        # 处理特定网络错误
        except ConnectionResetError as e:
            st.warning(f"连接中断，尝试重新连接 ({attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)  # 等待后重试
            else:
                # 多次失败后显示详细错误信息
                st.error(f"❌ 多次尝试后仍失败: {str(e)}")
                # 提供解决建议
                st.info("建议：")
                st.info("1. 检查网络连接是否稳定")
                st.info("2. 尝试更换网络环境")
                st.info("3. 稍后再试或联系DeepSeek支持")

        # 处理其他异常
        except Exception as e:
            st.error(f"生成失败: {str(e)}")
            st.info("请检查API密钥是否正确或稍后再试")
            break  # 其他错误不重试