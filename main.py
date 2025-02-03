import pygame
import sys
import threading
from src.audio_processing.speech_input import SpeechInput

#from src.audio_processing.deepseek_api import OpenAIAPI
from src.audio_processing.openai_api import OpenAIAPI

from src.audio_processing.tts_synthesis import TTSSynthesis
from src.video_processing import VideoProcessing
from src.utils.threading_utils import ThreadManager
from src.utils.pygame_utils import PyGameDisplay

global_scores = {
    "gryffindor": 0,
    "hufflepuff": 0,
    "ravenclaw": 0,
    "slytherin": 0
}

def main():
    pygame.init()

    exit_requested = False
    exit_lock = threading.Lock()

    speech_input = SpeechInput()
    openai_api = OpenAIAPI()
    tts_synthesis = TTSSynthesis()
    video_processing = VideoProcessing()
    thread_manager = ThreadManager()
    pygame_display = PyGameDisplay()

    thread_manager.start_thread(video_processing.process_video)

    def speech_input_thread():
        nonlocal exit_requested, exit_lock 
        while True:
            
            # 切换为语音输入
            #user_input = speech_input.get_speech()
            
            user_input = input("Enter your text: ")
            if user_input:
                response = openai_api.process_text(user_input)
                
                tts_synthesis.synthesize_speech(response.hat_response)
                
                global_scores["gryffindor"] += response.gryffindor
                global_scores["hufflepuff"] += response.hufflepuff
                global_scores["ravenclaw"] += response.ravenclaw
                global_scores["slytherin"] += response.slytherin
                
                print(f"\n\n当前分数: Gryffindor={global_scores['gryffindor']}, "
                      f"Hufflepuff={global_scores['hufflepuff']}, "
                      f"Ravenclaw={global_scores['ravenclaw']}, "
                      f"Slytherin={global_scores['slytherin']}")

                if (global_scores["gryffindor"] > 15 or
                    global_scores["hufflepuff"] > 15 or
                    global_scores["ravenclaw"] > 15 or
                    global_scores["slytherin"] > 15):
                    
                    print(f"学院已分配: Gryffindor={global_scores['gryffindor']}, "
                          f"Hufflepuff={global_scores['hufflepuff']}, "
                          f"Ravenclaw={global_scores['ravenclaw']}, "
                          f"Slytherin={global_scores['slytherin']}")

                    with exit_lock:
                        exit_requested = True
                    return 

    thread_manager.start_thread(speech_input_thread)

    running = True
    while running:
        with exit_lock:
            if exit_requested:
                running = False
                break 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame_display.update_display(video_processing.get_frame())

    thread_manager.stop_all_threads()
    video_processing.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
