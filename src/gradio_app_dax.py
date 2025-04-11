import gradio as gr
import speech_recognition as sr
import pyttsx3
import threading
import requests
import time
import librosa
import numpy as np
import sounddevice as sd
from scipy.spatial.distance import cdist

# === Configuration ===
API_URL = "http://localhost:5000/classify"
ACTIVATION_SAMPLE_PATH = "hello_dax_sample.wav"  # Your pre-recorded "Hello DAX"
WAKE_THRESHOLD = 80  # Tune this value depending on environment

# === Load Wake Word Sample ===
ref_audio, sr = librosa.load(ACTIVATION_SAMPLE_PATH, sr=16000)
ref_mfcc = librosa.feature.mfcc(y=ref_audio, sr=sr, n_mfcc=13)

# === TTS Engine ===
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def is_hello_dax(input_audio, sr=16000, threshold=WAKE_THRESHOLD):
    input_mfcc = librosa.feature.mfcc(y=input_audio, sr=sr, n_mfcc=13)
    dist = np.min(cdist(ref_mfcc.T, input_mfcc.T, metric='euclidean'))
    print(f"Wake word distance: {dist}")
    return dist < threshold

def record_audio(duration=2):
    print("🎤 Listening...")
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
    sd.wait()
    return audio.squeeze()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except:
            return ""

# === Background Voice Assistant Loop ===
def voice_assistant_loop(ui_refs):
    while True:
        audio = record_audio(duration=2)
        if is_hello_dax(audio):
            ui_refs["floating"].visible = True
            speak("Yes, I am here")

            command = listen_for_command()

            try:
                response = requests.post(API_URL, json={"text": command})
                intent = response.json().get("intent", "Unknown")
            except Exception as e:
                intent = f"[Backend error] {str(e)}"

            speak(intent)
            ui_refs["floating"].visible = False
            time.sleep(1)

        time.sleep(1)

# === Launch Gradio Interface ===
def start_gradio():
    with gr.Blocks(css="""
    .phone {
        width: 360px;
        height: 700px;
        margin: auto;
        border: 16px solid #333;
        border-radius: 36px;
        background: #fff;
        position: relative;
        padding: 0;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }
    .floating-ball {
        width: 70px;
        height: 70px;
        background-color: #4CAF50;
        border-radius: 50%;
        position: absolute;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 28px;
        box-shadow: 0 0 15px rgba(0,0,0,0.4);
    }
    """) as demo:

        with gr.Column(elem_classes="phone"):
            floating = gr.HTML("<div class='floating-ball'>🎤</div>", visible=False)

        ui_refs = {
            "floating": floating,
        }

        threading.Thread(target=voice_assistant_loop, args=(ui_refs,), daemon=True).start()
        demo.launch()

if __name__ == "__main__":
    start_gradio()