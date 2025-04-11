import gradio as gr
import speech_recognition as sr

# Speech recognition function
def transcribe_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "⏱️ Listening timed out."
        except sr.UnknownValueError:
            return "❓ Could not understand audio."
        except sr.RequestError:
            return "⚠️ API unavailable."

# Gradio interface with phone-style layout
with gr.Blocks(css="""
.phone {
    width: 360px;
    height: 700px;
    margin: auto;
    border: 16px solid #333;
    border-radius: 36px;
    background: #f9f9f9;
    padding: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.2);
}
""") as demo:
    with gr.Column(elem_classes="phone"):
        gr.Markdown("## 📱 Grab Voice Assistant")
        output_box = gr.Textbox(label="What you said", lines=3)
        listen_button = gr.Button("🎧 Start Listening")
        listen_button.click(fn=transcribe_audio, outputs=output_box)

demo.launch()
