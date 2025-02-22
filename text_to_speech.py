from gtts import gTTS
import os
import tempfile
import sys
from playsound import playsound

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_filename = fp.name
        tts.save(temp_filename)
    
    try:
        playsound(temp_filename)
    except Exception as e:
        print(f"Error playing sound: {e}")
    
    os.remove(temp_filename)
