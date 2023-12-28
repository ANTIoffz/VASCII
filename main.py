import math
import os
from os import system, mkdir, path
from shutil import get_terminal_size
from glob import glob
from datetime import timedelta, datetime
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, imwrite
from PIL import Image
from sys import stdout


VIDEOS_FOLDER = 'videos'
FRAMES_FOLDER = 'frames'
DYNAMIC_CHARS = 0
CLEAR_MODE = 2
REPEAT = 1

folders = ['frames', 'videos', 'audio']

def init():
    for folder in folders:
        if not path.exists(folder):
            os.mkdir(folder)

    if not path.exists('chars.txt'):
        with open('chars.txt', 'w+', encoding='utf-8') as file:
            file.write(' .,:;"*+/!?&%#@')



def clear_console():
    system('cls')


def get_chars():
    with open('chars.txt', 'r+', encoding='utf-8') as file:
        return list(file.read())


def get_video_data(video_path: str):
    videoCapture = VideoCapture()
    videoCapture.open(video_path)
    fps = int(videoCapture.get(CAP_PROP_FPS))
    frames_count = int(videoCapture.get(CAP_PROP_FRAME_COUNT))
    return fps, frames_count, videoCapture


def crate_frames(video_path: str, video_filename: str, frames_file_path: str):
    clear_console()
    fps, frames_count, videoCapture = get_video_data(video_path)
    print("Создание кадров")
    print(f"FILENAME: {video_filename}")
    print(f"FPS: {fps}")
    print(f"FRAMES: {frames_count}")
    print()

    mkdir(frames_file_path)
    for frame_number in range(int(frames_count)):
        _, frame = videoCapture.read()
        imwrite(f"{frames_file_path}/{frame_number}.jpg", frame)
    
    

def start_video(video_path: str, chars_list: list):
    clear_console()
    video_filename = video_path.split('{}\\'.format(VIDEOS_FOLDER))[1]
    frames_file_path = f'{FRAMES_FOLDER}\\{video_filename}'
    if not path.exists(frames_file_path):
        crate_frames(video_path, video_filename, frames_file_path)

    division = round(256 / len(chars_list), 2)
    fps, frames_count, videoCapture = get_video_data(video_path)
    start_time = datetime.now()
    for frame_number in range(frames_count):
        if DYNAMIC_CHARS:
            chars_list = get_chars()
            division = round(256 / len(chars_list), 2)
            
        next_frame = True
        terminal_y = get_terminal_size().lines
        terminal_x = get_terminal_size().columns
        img = Image.open(f"{frames_file_path}/{frame_number}.jpg").resize((terminal_x, terminal_y)).convert('L')
        while True:
            current_time = datetime.now() - start_time
            if current_time.total_seconds() >= timedelta(seconds=frame_number / fps).total_seconds():
                if current_time.total_seconds() >= timedelta(seconds=(frame_number + 1) / fps).total_seconds():
                    stdout.write(f"\rSKIPPED {frame_number}\r")
                    next_frame = False
                    break

                if CLEAR_MODE == 1:
                    clear_console()
                
                elif CLEAR_MODE == 2:
                    stdout.write("\033[H\033[J")
                
                for pixel in list(img.getdata()):
                    symbol_id = math.floor(pixel / division)
                    stdout.write(chars_list[symbol_id])
                    
                break
        if next_frame:
            stdout.write("\n")



def main_menu():
    while True:
        clear_console()
        chars_list = get_chars()
        print(f"Chars list = {' '.join(chars_list)}")
        print('')
        print("Choose mp4 video")

        videos = glob(f'{VIDEOS_FOLDER}\\*.mp4')
        for number, video in enumerate(videos, 1):
            print(f"[{number}] : {video}")

        selected_video = input()
        if not selected_video or not selected_video.isdigit() or 1 < int(selected_video) > len(videos):
            continue
        
        while True:
            try:
                start_video(videos[int(selected_video) - 1], chars_list)
                if not REPEAT:
                    break
            except KeyboardInterrupt:
                break


def main():
    init()
    while True:
        main_menu()


if __name__ == '__main__':
    main()
