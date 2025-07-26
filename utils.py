# 导入必要的库
from langchain.prompts import ChatPromptTemplate  # 用于构建聊天提示模板
from langchain_openai import ChatOpenAI  # LangChain的OpenAI聊天模型封装
import requests  # 用于发送HTTP请求
import json  # JSON数据处理


# API连接测试函数
def test_api_connection(api_key):
    """
    测试DeepSeek API连接是否有效

    参数:
        api_key (str): DeepSeek API密钥

    返回:
        bool: 连接成功返回True，否则返回False
    """
    try:
        # API端点配置
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",  # 认证头
            "Content-Type": "application/json"  # 内容类型
        }
        data = {
            "model": "deepseek-chat",  # 使用的模型
            "messages": [{"role": "user", "content": "测试连接，请回复'连接成功'"}],  # 测试消息
            "temperature": 0.7,  # 生成随机性
            "max_tokens": 10  # 限制响应长度
        }

        # 发送POST请求（设置10秒超时）
        response = requests.post(url, json=data, headers=headers, timeout=10)

        # 检查响应状态码
        return response.status_code == 200  # 200表示成功
    except Exception:
        # 捕获所有异常（网络错误/超时等）
        return False


# 主功能函数：生成视频脚本
def generate_script(subject, video_length, creativity, api_key):
    """
    根据主题生成视频标题和脚本

    参数:
        subject (str): 视频主题内容
        video_length (int): 视频时长（分钟）
        creativity (float): 创意度参数（0.0-1.0）
        api_key (str): DeepSeek API密钥

    返回:
        tuple: (search_result, title, script)
            search_result: 维基百科搜索结果
            title: 生成的视频标题
            script: 生成的视频脚本

    异常:
        抛出生成失败的具体错误信息
    """
    # ================== 提示模板配置 ==================
    # 标题生成模板（单轮对话）
    title_template = ChatPromptTemplate.from_messages(
        [("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")]
    )

    # 脚本生成模板（带结构化要求）
    script_template = ChatPromptTemplate.from_messages(
        [("human",
          """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
          视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
          要求：
          - 开头直接切入主题（1-2句话）
          - 中间只保留核心干货（3-5个要点）
          - 结尾简短有力（1-2句话）
          - 整体语言精炼，避免冗余
          参考信息（可选使用）：
          ```{wikipedia_search}```""")]
    )

    # ================== 模型配置 ==================
    # 创建DeepSeek聊天模型实例（关键修改点）
    model = ChatOpenAI(
        model_name="deepseek-chat",  # 指定模型
        openai_api_key=api_key,  # 传入API密钥
        temperature=creativity,  # 控制生成随机性（0=严谨, 1=创意）
        openai_api_base="https://api.deepseek.com/v1",  # 自定义API端点
        max_tokens=2048,  # 减少token数量控制输出长度
        request_timeout=30,  # 设置超时时间（秒）
        max_retries=2  # 添加失败重试机制
    )

    # ================== 处理链构建 ==================
    # 构建标题生成链：模板 -> 模型
    title_chain = title_template | model
    # 构建脚本生成链：模板 -> 模型
    script_chain = script_template | model

    # ================== 标题生成 ==================
    try:
        # 调用模型生成标题
        title = title_chain.invoke({"subject": subject}).content

    except Exception as e:
        # 捕获并封装异常
        raise Exception(f"标题生成失败: {str(e)}")

    try:
        # 调用模型生成脚本（传入标题/时长/搜索内容）
        script = script_chain.invoke({
            "title": title,
            "duration": video_length,
            "wikipedia_search": "未找到相关信息"



        }).content
    except Exception as e:
        # 捕获并封装异常
        raise Exception(f"脚本生成失败: {str(e)}")

    return title, script
