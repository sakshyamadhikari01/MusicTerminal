import os
import time
import sys
import threading
import pygame

GREEN = '\033[38;2;30;215;96m'
WHITE = '\033[38;2;255;255;255m'
GRAY = '\033[38;2;83;83;83m'
RESET = '\033[0m'
control = {"command": "", "running": True, "playing": True}
def progress_thread(folder_path):
    pygame.mixer.init()
    songs = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
    for song in songs:
        if not control["running"]: break
        path = os.path.join(folder_path, song)
        pygame.mixer.music.load(path)
        total_len = pygame.mixer.Sound(path).get_length()
        pygame.mixer.music.play()
        control["playing"] = True
        while pygame.mixer.music.get_busy() or not control["playing"]:
            if not control["running"]: return
            if control["command"] == "stop" and control["playing"]:
                pygame.mixer.music.pause()
                control["playing"] = False
                control["command"] = "" 
            elif control["command"] == "play" and not control["playing"]:
                pygame.mixer.music.unpause()
                control["playing"] = True
                control["command"] = ""
            elif control["command"] == "skip":
                pygame.mixer.music.stop()
                control["command"] = ""
                break 
            pos = pygame.mixer.music.get_pos() / 1000
            if pos < 0: pos = total_len
            progress = min(pos / total_len, 1.0)
            bar = f"{GREEN}{'━' * int(30 * progress)}○{RESET}{GRAY}{'━' * (30 - int(30 * progress))}{RESET}"
            sys.stdout.write(f"\r  {bar} | {song[:15]}... ")
            sys.stdout.flush()
            time.sleep(0.1)
    print(f"\n{GREEN}Music queue finished.{RESET}")
def start():
    path = input("Enter Music Folder: ").strip('"')
    if not os.path.isdir(path): return
    threading.Thread(target=progress_thread, args=(path,), daemon=True).start()
    print(f"\nCommands: {WHITE}'stop'{RESET}, {WHITE}'play'{RESET}, {WHITE}'skip'{RESET}, {WHITE}'exit'{RESET}")
    while control["running"]:
        user_input = input("\nAction: ").lower().strip()
        if user_input == "exit":
            control["running"] = False
            print("Shutting down...")
        else:
            control["command"] = user_input
if __name__ == "__main__":
    start()
                        
                        