import datetime
from time import time
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import win32api
import os
import subprocess
import json
import wolframalpha
import requests
import pyjokes
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Leafy, how can I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("I didn't quite catch that, can you please repeat?")
        return "None"
    return query

if __name__== "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
             speak('Searching wikipedia...')
             query = query.replace("wikipedia","")
             results = wikipedia.summary(query, sentences=2)
             speak("According to Wikipedia")
             print(results)
             speak(results)

        elif "word" in query:
            speak("Opening Adobe Photoshop 2021")
            print("Opening Adobe Photoshop 2021")
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Photoshop 2021.lnk")

        elif "Photoshop" in query:
            speak("Opening Microsoft Word 2016")
            print("Opening Microsoft Word 2016")
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word 2016.lnk")

        elif "code" in query:
            speak("Opening Visual Studio Code")
            print("Opening Visual Studio Code")
            os.startfile("C:\\Users\\Kahsish Khan\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk")

        elif 'joke' in query:
            speak(pyjokes.get_joke(language='en', category= 'all'))

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you doing?")

        elif 'fine' in query or "good" in query:
            speak("I'm glad")

        elif 'upset' in query or "sad" in query:
            speak("It is ok, things will get better for you I am sure.")
            speak("Do you want me to cheer you up with a joke?")
            speak("If you do then you need only ask for it.")

        elif "who i am" in query:
            speak("If you talk then definitely your human.")

        elif "why do you exist" in query:
            speak("I am Kashish's final year project, and also to help others out!")

        elif 'youtube' in query:
            speak('At your service!')
            webbrowser.open("youtube.com")

        elif 'google' in query:
            speak('At your service!')
            webbrowser.open("google.com")

        elif 'headlines' in query or "news" in query:

            try:
                jsonObj = url("https://newsapi.org//v1//articles?source = the-times-of-india&sortBy = 81d89036c7f644cc90afa75866b7ee7c =\\times of India Api key\\")
                data = json.load(jsonObj)
                i = 1
                 
                speak('here are some top news from the times of india')
                print('''=============== TIMES OF INDIA ============'''+ '\n')
                 
                for item in data['articles']:
                     
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                 
                print(str(e))
 

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
             
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "shutdown" in query or "turnoff" in query:
            speak("Hibernating")
            subprocess.call("shutdown / s")

        elif "log off" in query or "sign out" in query:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif 'time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'search'  in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            time.sleep(5)

        elif 'empty recycle bin' in query:
            win32api.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Recycle Bin Recycled")

        elif "calculate" in query or "what is" in query:
             
            app_id = "WVQW42-4XEJ25LEYJ"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif "bye" in query or "see ya later" in query or "stop" in query:
            speak('Leafy, Signing out!')
            print('Leafy, Signing out!')
            break
