
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY


elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str , folder : str) -> str:
    # Prepare the full folder path under user_uploads
    folder_path = os.path.join("user_uploads", folder)
    os.makedirs(folder_path, exist_ok=True)  # make sure it exists

    # Calling the ElevenLabs text-to-speech API
    response = elevenlabs.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    save_file_path = os.path.join(folder_path, "audio.mp3")

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    return save_file_path
