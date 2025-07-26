# 🎬 基于DeepSeek大模型API 视频脚本生成器

**使用 Python + DeepSeek API 自动生成视频脚本** |  [API文档](https://platform.deepseek.com/api-docs/)



[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange?logo=openai)](https://deepseek.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 核心功能

- **一键生成**：输入主题关键词，自动生成视频脚本

- **支持下载**：可以下载生成的脚本文件，格式为.txt

##  快速开始

### 前置要求
1. 获取 [DeepSeek API Key](https://platform.deepseek.com/)
2. Python 3.8+
3. pycharm软件

## ⚠️ 法律声明

### 1. 无担保条款
本软件按"**现状**"提供，开发者**不作任何明示或暗示的担保**，包括但不限于：
- 适销性担保
- 特定用途适用性担保
- 权利完整性担保

### 2. 风险承担
使用者需自行承担使用风险，包括：
- 因API调用产生的费用损失
- 生成内容导致的版权纠纷
- 数据丢失或业务中断风险

### 3. 责任限制
在任何情况下，开发者**不对因使用或无法使用本软件导致的任何直接/间接损失负责**。

### 4. 内容责任
生成内容基于AI模型输出：
- 不代表开发者观点
- 请人工审核并遵守平台规范
- 禁止用于违法用途

### 安装
```bash
# 克隆项目
git clone https://github.com/XUKAI2002/Video-script-generator.git

# 安装依赖(requirements.txt文件见主项目)
pip install -r requirements.txt

# 运行项目
streamlit run main.py
