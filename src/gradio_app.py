import gradio as gr
import speech_recognition as sr
import requests

API_URL = "http://localhost:5000/classify"  # Flask backend URL

def transcribe_and_classify():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return "⏱️ Listening timed out.", ""
        except sr.UnknownValueError:
            return "❓ Could not understand audio.", ""
        except sr.RequestError:
            return "⚠️ API unavailable.", ""

    try:
        response = requests.post(API_URL, json={"text": text})
        if response.status_code == 200:
            intent = response.json()["intent"]
        else:
            intent = "Error getting intent."
    except Exception as e:
        intent = f"Failed to contact backend: {e}"

    return text, intent

# Gradio UI
with gr.Blocks(css="""
.phone {
    width: 360px;
    height: 700px;
    margin: auto;
    border: 16px solid #333;
    border-radius: 36px;
    background: #f1f1f1;
    padding: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.2);
}
""") as demo:
    with gr.Column(elem_classes="phone"):
        gr.Markdown("## 📱 Grab Assistant (Voice)")
        transcript = gr.Textbox(label="You said", lines=2)
        prediction = gr.Textbox(label="Predicted Intent", lines=1)
        listen_button = gr.Button("🎧 Start Listening")
        listen_button.click(fn=transcribe_and_classify, outputs=[transcript, prediction])

demo.launch()
