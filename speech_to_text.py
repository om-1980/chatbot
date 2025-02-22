import speech_recognition as sr

def listen_and_transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (speak now)")
        audio = r.listen(source)
    try:
        print("Transcribing...")
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Error with the request; {0}".format(e))
        return ""
