# This file looks for new folders inside 'user_uploads'and covert them into reel
import os
import time
import subprocess

from text_to_audio import text_to_speech_file

def text_to_audio(folder):
    folder_path = os.path.join("user_uploads", folder)
    desc_file = os.path.join(folder_path, "desc.txt")
    with open(desc_file) as file:
        text = file.read()
    print(text , folder)
    text_to_speech_file(text , folder)


def create_reel(folder):
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt \
    -i user_uploads/{folder}/audio.mp3 \
    -vf "scale=1080:1920:force_original_aspect_ratio=decrease,\
    pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
    -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p \
    static/reels/{folder}.mp4'''
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    while True:
        print("Processing queue...")
        with open("done.txt", "r") as f:
            done_folders = f.readlines()

        done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_uploads")

        for folder in folders:
            if os.path.isdir(os.path.join("user_uploads", folder)):
                if folder not in done_folders:
                    text_to_audio(folder)
                    create_reel(folder)
                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")
        time.sleep(4)