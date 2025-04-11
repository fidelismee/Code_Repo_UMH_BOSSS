import tkinter as tk
import speech_recognition as sr
import pyttsx3
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Chatbot GUI
class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grab Assistant")
        self.chat_log = tk.Text(root, bg="white", height=20, width=50)
        self.chat_log.pack()
        self.chat_log.insert(tk.END, "Say 'Hello Grab' to activate assistant...\n")
        self.chat_log.config(state=tk.DISABLED)

    def show_message(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

# Voice Activation
def listen_for_activation(gui):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        gui.show_message("Listening for activation...")

    while True:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print("Heard:", command)
                if "hello grab" in command:
                    respond_to_user(gui)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                gui.show_message("API unavailable.")
                break

# Respond function
def respond_to_user(gui):
    response = "Hi! I'm your Grab Assistant. How can I help you?"
    engine.say(response)
    engine.runAndWait()
    gui.show_message("Grab Assistant: " + response)

# Main GUI thread
def run_gui():
    root = tk.Tk()
    gui = ChatBotGUI(root)
    threading.Thread(target=listen_for_activation, args=(gui,), daemon=True).start()
    root.mainloop()

run_gui()

