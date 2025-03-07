import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return ""

def jarvis():
    speak("Hello, I am Jarvis. How can I assist you?")
    while True:
        command = listen()
        if "time" in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {now}")
        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "play music" in command:
            speak("Playing music")
            os.system("start wmplayer")  # Works on Windows, change for other OS
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    jarvis()