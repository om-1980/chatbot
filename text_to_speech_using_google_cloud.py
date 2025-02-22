from google.cloud import texttospeech
from google.oauth2 import service_account
import os
import tempfile
from playsound import playsound

# Replace this with the path to your JSON key file
CREDENTIALS_PATH = "buoyant-operand-450310-i7-1b9fbccfbb5a.json"

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)


def speak_text(text):
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_filename = fp.name
        fp.write(response.audio_content)

    try:
        playsound(temp_filename)
    except Exception as e:
        print(f"Error playing sound: {e}")

    os.remove(temp_filename)
