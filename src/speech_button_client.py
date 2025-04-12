import tkinter as tk
import speech_recognition as sr
import requests
import pyttsx3

APP_URL = "http://localhost:5000/classify"
FORWARD_URL = "http://localhost:6000/process"

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_and_send():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        label.config(text="🟢 Speak now (you have 7 seconds)...")
        speak("I'm listening.")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
            label.config(text="⏳ Processing...")

            # Speech-to-text
            command = recognizer.recognize_google(audio).lower()
            print("🧠 Heard:", command)
            speak(f"You said: {command}")

            # Classifier
            classify_resp = requests.post(APP_URL, json={"text": command})
            intent = classify_resp.json().get("intent", "unknown")
            print("🎯 Intent from app.py:", intent)

            # Forwarding
            forward_resp = requests.post(FORWARD_URL, json={"text": intent})
            structured = forward_resp.json()
            print("📦 JSON Output:", structured)

            # UI Output
            result_text = (
                f"🔊 Heard: {command}\n"
                f"🎯 Intent (from app.py): {intent}\n"
                f"📦 Structured JSON:\n{structured}"
            )

            result_box.config(state="normal")
            result_box.delete("1.0", tk.END)
            result_box.insert(tk.END, result_text)
            result_box.config(state="disabled")

            label.config(text="✅ Success!")
            speak(f"The output from app dot pie is: {intent}")


        except sr.WaitTimeoutError:
            label.config(text="⏱️ You didn’t speak in time. Try again.")
            speak("You didn’t speak in time. Please try again.")
        except sr.UnknownValueError:
            label.config(text="🤷 Speech not understood. Try again.")
            speak("Sorry, I couldn't understand that.")
        except Exception as e:
            label.config(text=f"❌ Error: {str(e)}")
            print("❌ Exception:", e)
            speak("An error occurred.")


# GUI setup
root = tk.Tk()
root.title("DAX Voice Interface")
root.geometry("400x500")

label = tk.Label(root, text="Click to Speak", font=("Helvetica", 16))
label.pack(pady=20)

btn = tk.Button(root, text="🎤 Speak Now", font=("Helvetica", 14), command=recognize_and_send)
btn.pack(pady=10)

result_box = tk.Text(root, height=15, width=45, wrap="word", state="disabled")
result_box.pack(pady=10)

root.mainloop()