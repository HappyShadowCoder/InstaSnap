import os
import time
import subprocess
from gtts import gTTS

try:
    from elevenlabs import generate, save
    ELEVEN_AVAILABLE = True
except ImportError:
    ELEVEN_AVAILABLE = False


def text_to_audio(text, folder):
    output_path = os.path.join("user_uploads", folder, "audio.mp3")

    if ELEVEN_AVAILABLE:
        try:
            print(f"[INFO] Attempting ElevenLabs TTS for folder: {folder}")
            audio = generate(
                text=text,
                voice="Rachel",
                model="eleven_monolingual_v1"
            )
            save(audio, output_path)
            print(f"[SUCCESS] ElevenLabs audio saved for {folder}")
            return
        except Exception as e:
            print(f"[WARNING] ElevenLabs failed: {e}")

    try:
        print(f"[INFO] Falling back to gTTS for folder: {folder}")
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        print(f"[SUCCESS] gTTS audio saved for {folder}")
    except Exception as e:
        print(f"[ERROR] gTTS also failed: {e}")


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
            done_folders = [line.strip() for line in f.readlines()]

        folders = os.listdir("user_uploads")

        for folder in folders:
            if os.path.isdir(os.path.join("user_uploads", folder)) and folder not in done_folders:
                desc_path = os.path.join("user_uploads", folder, "desc.txt")
                if os.path.exists(desc_path):
                    with open(desc_path, "r") as file:
                        text = file.read()
                    text_to_audio(text, folder)
                    create_reel(folder)
                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")
                else:
                    print(f"[WARNING] No desc.txt in {folder}. Skipping.")

        time.sleep(6)
