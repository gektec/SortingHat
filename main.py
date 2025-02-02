import pygame
import sys
from src.audio_processing.speech_input import SpeechInput
from src.audio_processing.openai_api import OpenAIAPI
from src.audio_processing.tts_synthesis import TTSSynthesis
from src.video_processing import VideoProcessing
from src.utils.threading_utils import ThreadManager
from src.utils.pygame_utils import PyGameDisplay

def main():
    # 初始化Pygame
    pygame.init()

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
        while True:
            speech_text = speech_input.get_speech()
            if speech_text:
                # 调用OpenAI API处理语音文本
                response_text = openai_api.process_text(speech_text)
                # 合成语音
                tts_synthesis.synthesize_speech(response_text)

    # 启动语音输入线程
    thread_manager.start_thread(speech_input_thread)

    # 主循环
    running = True
    while running:
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
