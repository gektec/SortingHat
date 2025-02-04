# SortingHat

## Usage
需求python版本：3.9-3.12

1. `pip install -r requirements.txt`

2. `python main.py`

## 说明

### AI/游戏性

该SortingHat利用评分机制为user选择合适的学院。user的输入会经过LLM评分，输出为json并进行计算。AI允许连续对话。

### GUI/IO

目前输入功能包含控制台及google语音输入（已被注释）。
在pygame窗口中进行输入需要较多工作。我正考虑使用pyqt重写。

### ai多模态

我认为在该项目中，ai的多模态特性难以应用。因此我仅使用python库进行音频及视频处理，部分提升沉浸感。

### API
我已将我的私人api写入`config.json` 。在`main.py`中可通过注释选择deepseek或openai。

### 语音合成部分

我研究后发现主流声音合成引擎无法为Sorting Hat提供合适的音色，因此我决定略过该部分，仅通过调用本地合成引擎简单合成。
