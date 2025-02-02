import pygame
import sys
import threading  # 新增导入
from src.audio_processing.speech_input import SpeechInput
from src.audio_processing.deepseek_api import OpenAIAPI
from src.audio_processing.tts_synthesis import TTSSynthesis
from src.video_processing import VideoProcessing
from src.utils.threading_utils import ThreadManager
from src.utils.pygame_utils import PyGameDisplay

# 全局变量来存储各个学院的分数
global_scores = {
    "gryffindor": 0,
    "hufflepuff": 0,
    "ravenclaw": 0,
    "slytherin": 0
}

def main():
    # 初始化Pygame
    pygame.init()

    # 退出标志和锁
    exit_requested = False
    exit_lock = threading.Lock()

    # 初始化各个模块
    speech_input = SpeechInput()
    openai_api = OpenAIAPI()
    tts_synthesis = TTSSynthesis()
    video_processing = VideoProcessing()
    thread_manager = ThreadManager()
    pygame_display = PyGameDisplay()

    # 启动视频处理线程
    thread_manager.start_thread(video_processing.process_video)

    # 语音输入线程
    def speech_input_thread():
        nonlocal exit_requested, exit_lock  # 允许修改外部变量
        while True:
            #user_input = speech_input.get_speech()
            user_input = input("Enter your text: ")
            if user_input:
                # 调用OpenAI API处理语音文本
                response = openai_api.process_text(user_input)
                
                # 更新全局分数
                global_scores["gryffindor"] += response.gryffindor
                global_scores["hufflepuff"] += response.hufflepuff
                global_scores["ravenclaw"] += response.ravenclaw
                global_scores["slytherin"] += response.slytherin
                
                # 打印当前分数
                print(f"当前分数: Gryffindor={global_scores['gryffindor']}, "
                      f"Hufflepuff={global_scores['hufflepuff']}, "
                      f"Ravenclaw={global_scores['ravenclaw']}, "
                      f"Slytherin={global_scores['slytherin']}")
                
                # 检查学院分数是否超过20
                if (global_scores["gryffindor"] > 20 or
                    global_scores["hufflepuff"] > 20 or
                    global_scores["ravenclaw"] > 20 or
                    global_scores["slytherin"] > 20):
                    # 打印结果
                    print(f"学院分数超过20: Gryffindor={global_scores['gryffindor']}, "
                          f"Hufflepuff={global_scores['hufflepuff']}, "
                          f"Ravenclaw={global_scores['ravenclaw']}, "
                          f"Slytherin={global_scores['slytherin']}")
                    # 设置退出标志
                    with exit_lock:
                        exit_requested = True
                    return  # 退出当前线程
                
                # 合成语音
                tts_synthesis.synthesize_speech(response.hat_response)

    # 启动语音输入线程
    thread_manager.start_thread(speech_input_thread)

    # 主循环
    running = True
    while running:
        # 检查退出标志
        with exit_lock:
            if exit_requested:
                running = False
                break  # 立即退出循环

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新显示
        pygame_display.update_display(video_processing.get_frame())

    # 释放资源
    thread_manager.stop_all_threads()
    video_processing.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
