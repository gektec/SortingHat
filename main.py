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


def main():
    pygame.init()

    exit_requested = False
    exit_lock = threading.Lock()
    cumulative_scores = {"Gryffindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0}

    speech_input = SpeechInput()
    openai_api = OpenAIAPI()
    tts_synthesis = TTSSynthesis()
    video_processing = VideoProcessing()
    thread_manager = ThreadManager()
    pygame_display = PyGameDisplay()

    initial_prompt = "Welcome to Hogwarts! Show yourself."
    print(initial_prompt)
    tts_synthesis.synthesize_speech(initial_prompt)  # Using TTS to read the prompt aloud

    thread_manager.start_thread(video_processing.process_video)

    def speech_input_thread():
        nonlocal exit_requested, exit_lock 
        while True:
            
            # 切换为语音输入
            #user_input = speech_input.get_speech()
            
            user_input = input("\nEnter your text: ")  # User input through console
            
            if user_input:
                response = openai_api.process_text(user_input)
                
                tts_synthesis.synthesize_speech(response.hat_response)  # Use TTS for the response
                
                cumulative_scores["Gryffindor"] += response.gryffindor
                cumulative_scores["Hufflepuff"] += response.hufflepuff
                cumulative_scores["Ravenclaw"] += response.ravenclaw
                cumulative_scores["Slytherin"] += response.slytherin
                
                print("\nCurrent Scores:")
                for house, score in cumulative_scores.items():
                    print(f"{house}: {score}")

                # Exiting conditions based on score
                if any(score > 15 for score in cumulative_scores.values()):
                    print("\nHouse with highest score:")
                    winner = max(cumulative_scores, key=cumulative_scores.get)
                    print(f"{winner} with a score of {cumulative_scores[winner]}")

                    with exit_lock:
                        exit_requested = True
                    return 

    thread_manager.start_thread(speech_input_thread)

    # Main Pygame event loop
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
