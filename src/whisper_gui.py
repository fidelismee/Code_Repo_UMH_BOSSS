from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json

model = Model("model")  # Download from: https://alphacephei.com/vosk/models
recognizer = KaldiRecognizer(model, 16000)

def listen_vosk(duration=5):
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    if recognizer.AcceptWaveform(audio.tobytes()):
        result = json.loads(recognizer.Result())
        print("📝 Text:", result.get("text", ""))
        return result.get("text", "")
    return ""
