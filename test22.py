import tkinter as tk
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from playsound import playsound
import random
import threading
import pyaudio
import time
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

running = False  
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
if numdevices>2:
    dev_index=1
else:
    dev_index=0

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("good morning sir")
    elif hour >= 12 and hour < 5:
        speak("good afternoon sir")
    else:
        speak("good evening sir")
    speak("how may i help you")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=dev_index) as source:
        print('Listening...')
        r.pause_threshold = 2
        r.energy_threshold = 1000
        audio = r.listen(source)
    try:
        print('Recognizing')
        query = r.recognize_google(audio, language='en-in')
        print(f'you said {query}\n')
    except:
        print()
        print('say that again')
        return 'None'
    return query


def run_voice_assistant():
    global running
    running = True
    wishme()
    while running:
        query = takecommand().lower()
        print(query)
        if 'wikipedia' in query:
            speak('searching wikipedia')
            query = query.replace('wikipedia', '')
            if(query == ''):
                query = 'wikipedia'
            res = wikipedia.summary(query, sentences=2)
            speak('according to wikipedia...')
            speak(res)
        elif 'open google' in query:
            webbrowser.open('google.com')
        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
        elif 'open w3schools' in query:
            webbrowser.open('w3schools.com')
        elif 'play music' in query:
            md = "music"
            songs = os.listdir(md)
            n = random.randrange(len(songs))
            speak('playing now, please wait...')
            playsound(os.path.join(md, songs[n]))
        elif 'code' in query:
            os.startfile(
                "C:\\Users\\dh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        elif 'android studio' in query:
            os.startfile(
                "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe")
        elif 'notepad' in query:
            os.startfile("C:\\Windows\\notepad.exe")
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif 'joke' in query:
            joke = requests.get('https://official-joke-api.appspot.com/random_joke').json()
            speak(f"{joke['setup']}")
            time.sleep(1)
            speak(f"{joke['punchline']}")
        elif 'fact' in query:
            facts = requests.get('https://useless-facts.sameerkumar.website/api').json()['data']
            #fact = random.choice(facts)
            speak(facts)
            print(facts )
        elif 'create file' in query:
            speak('What do you want to name the file?')
            file_name = takecommand()
            if file_name != 'None':
                file_path = f"C:\\Users\\dh\\Desktop\\{file_name}.txt" 
                if os.path.exists(file_path):
                    speak(f"A file with the name {file_name} already exists on your desktop.")
                else:
                    file = open(file_path, 'w')
                    speak(f"File {file_name} has been created on your desktop.")
                    file.close()
            else:
                speak('Sorry, I did not hear the file name. Please try again.')
        elif 'bye' in query:
            speak('Bye sir,have a great day')
            break

def toggle_voice_assistant():
    global running
    if running:
        running = False
    else:
        threading.Thread(target=run_voice_assistant).start()

root = tk.Tk()
root.title("Voice Assistant")
root.geometry('180x210')
button = tk.Button(root, text="Start/Stop Voice Assistant", command=toggle_voice_assistant)
button.pack(side="bottom", pady=95, anchor="center")

root.mainloop()

