# SortingHat

## Usage
需求python版本：3.9-3.12

1. `pip install -r requirements.txt`

2. `python main.py`

## 说明

### 游戏性

该SortingHat利用评分机制为user选择合适的学院。user的输入会经过LLM评分，输出为json并进行计算。

### pygame

目前输入功能包含控制台及google语音输入（已被注释）。在pygame窗口中进行输入需要较多工作。

### ai多模态

我认为在该项目中，ai的多模态特性难以应用。因此我仅使用python库进行音频及视频处理，部分提升沉浸感。

### 语音合成部分

我研究后发现主流声音合成引擎无法为Sorting Hat提供合适的音色，因此我决定略过该部分，仅通过调用本地合成引擎简单合成。