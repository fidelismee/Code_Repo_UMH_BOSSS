import tkinter as tk
import speech_recognition as sr
import pyttsx3
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pickle

# === Load Model and Tokenizer ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "my_finetuned_bert"

tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

with open(f"{model_path}/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

def classify(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    return label_encoder.inverse_transform([pred])[0]

# === Initialize TTS ===
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# === Chatbot GUI ===
class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grab Assistant")
        
        self.chat_log = tk.Text(root, bg="white", height=20, width=60)
        self.chat_log.pack(padx=10, pady=10)
        self.chat_log.config(state=tk.DISABLED)

        self.listen_button = tk.Button(root, text="Start Listening 🎙️", command=self.listen_and_respond, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.listen_button.pack(pady=10)

    def show_message(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

    def listen_and_respond(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        self.show_message("🎧 Listening... Speak now.")
        
        try:
            with mic as source:
                recognizer.energy_threshold = 300
                recognizer.pause_threshold = 1
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=7)

            user_input = recognizer.recognize_google(audio)
            self.show_message("You: " + user_input)

            prediction = classify(user_input)
            self.show_message("Grab Assistant: " + prediction)

            engine.say(prediction)
            engine.runAndWait()

        except sr.WaitTimeoutError:
            self.show_message("⏰ Timeout: You didn’t say anything.")
        except sr.UnknownValueError:
            self.show_message("🤷 I couldn’t understand what you said.")
        except sr.RequestError:
            self.show_message("⚠️ Speech recognition service error.")


# === Run the App ===
def run_gui():
    root = tk.Tk()
    gui = ChatBotGUI(root)
    root.mainloop()

run_gui()
