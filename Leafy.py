import datetime
from time import time
from tkinter import *
from urllib.request import urlopen
import pyttsx3
import playsound
import speech_recognition as sr
import wikipedia
import webbrowser
import winshell
import os
import pyautogui
import subprocess
import json
import pyjokes
import time 
import psutil
from PIL import ImageTk,Image
import wolframalpha


engine = pyttsx3.init('sapi5') #sapi5 is the driver for windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #setting for choosing the voice 
engine.setProperty('rate', 160) #setting the speed of speech 
engine.setProperty('volume',1.0) # setting up volume level  between 0 and 1


def speak(audio):

    engine.say(audio)
    engine.runAndWait()


def takeCommand():

    r = sr.Recognizer() #to recognize our speech
    
    with sr.Microphone() as source: #input is a command given from the microphone
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

   
    query = ""


    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except sr.UnknownValueError:
        print("Assistant could not recognize the command")

    except sr.RequestError as ex:
        print("Request error from Google Speech Recognition" + ex)
   
    except Exception as e:
        print("I didn't quite catch that, can you please repeat?")
        speak("I didn't quite catch that, can you please repeat?")
        return "None"

    return query


def cpu():
    
    usage = str(psutil.cpu_percent())
    speak("CPU is at" + usage)
    battery = str(psutil.sensors_battery())
    speak("CPU is at" + battery)


def wishMe():

    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Leafy!")


def username():

    speak("What do people call you?")
    print("What do people call you?")
    uname=takeCommand()
    speak("Hello there, " + uname)
    print("Hello there, " + uname)
    speak("How may I help you?")        


def leafy():
    
    if __name__== "__main__":
        wishMe()
        username()
    

    while True:
        query = takeCommand().lower()


        if 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you doing?")


        elif 'fine' in query or "good" in query or "great" in query:
            speak("I'm glad")


        elif 'upset' in query or "sad" in query:
            speak("It is ok, things will get better for you, I am sure.")
            speak("Do you want me to cheer you up with a joke?")
            
            pr=takeCommand()

            if 'yes' in pr or 'sure' in pr or 'ok' in pr:
                speak(pyjokes.get_joke(language='en', category= 'neutral'))
                print(pyjokes.get_joke(language='en', category= 'neutral'))
            
            else:
                speak("Just trying to help")


        elif 'joke' in query:
            speak(pyjokes.get_joke(language='en', category= 'neutral'))
            print(pyjokes.get_joke(language='en', category= 'neutral'))


        elif "who am i" in query:            
            speak("You sound like you're human.")    


        elif "why do you exist" in query or "who are you" in query:
            speak("I am Kashish's final year project, and also I like to help people out!")


        elif "who made you" in query or "who is your creator" in query:
            speak("My creator is looking at the screen right now.") 

       
        elif "who do you look up to" in query or "who inspires you" in query:
            speak("I want to be as great as Alexa and Siri someday!")

       
        elif "inspiration behind your name" in query:
            speak("One fine day, while playing games in the computer lab, Kashish had an eureka moment")

        
        elif "do you have any friends" in query:
            speak("Yeah, one, it's Kashish!")     


        elif "play music" in query or "play songs" in query:
            dir = "D:\Leafy\music"
            music = os.listdir(dir)
            d = random.choice(music)
            random = os.path.join(dir, d)
            playsound.playsound(random)
            speak("Yeah, one, it's Kashish!")   


        elif "open photoshop" in query or "launch photoshop" in query:

            speak("Opening Adobe Photoshop 2021")
            print("Opening Adobe Photoshop 2021")
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Photoshop 2021.lnk")

        
        elif "open word" in query or "launch word" in query:

            speak("Opening Microsoft Word 2016")
            print("Opening Microsoft Word 2016")
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word 2016.lnk")

        
        elif "open code" in query or "launch code" in query:

            speak("Opening Visual Studio Code")
            print("Opening Visual Studio Code")
            os.startfile("C:\\Users\\Kahsish Khan\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk")

        
        elif "open chrome" in query or "launch chrome" in query:

            speak("Opening Google Chrome")
            print("Opening Google Chrome")
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk")

        
        elif "open maya" in query or "launch maya" in query:
            speak("Opening Maya 2022")
            print("Opening Maya 2022")
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Autodesk Maya 2022\\Maya 2022.lnk")

        
        elif "open counter strike" in query or "launch counter strike" in query:

            speak("Opening Counter-Strike: Global Offensive")
            print("Opening Counter-Strike: Global Offensive")
            os.startfile("C:\\Users\\Kahsish Khan\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Steam\\Counter-Strike Global Offensive.url")

        
        elif "open apex" in query or "launch apex" in query:

            speak("Opening Visual Studio Code")
            print("Opening Visual Studio Code")
            os.startfile("C:\\Users\\Kahsish Khan\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Steam\\Apex Legends.url")

       
        elif 'wikipedia' in query:
            
             speak('Searching wikipedia...')
             query = query.replace("wikipedia","")
             results = wikipedia.summary(query, sentences=2)
             speak("According to Wikipedia")
             print(results)
             speak(results)

       
        elif 'where is' in query:

            query = query.replace("where is" , "")
            location = query
            speak("Locating....")
            speak(location)
            webbrowser.open("https://www.google.com/maps/place/"+location+"")
            
       
        elif 'write a note' in query or 'make a note' in query:

            speak('OK, what would you like me to note down?')
            note = takeCommand()
            file = open('leafy.txt','w')
            speak("Do you want me to mention the date and time too?")
            sn=takeCommand()
     
            if 'yes' in sn or 'sure' in sn or 'yup' in sn:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(note)
                speak("Noted")
            
            else:
                file.write(note)
                speak("Noted")


        elif 'show notes' in query:

            speak('Here you go')
            file=open('leafy.txt','r')
            print(file.read())
            speak(file.read(6))


        elif 'open youtube' in query:

            speak('At your service!')
            webbrowser.open("youtube.com")


        elif 'open geeks for geeks' in query:

            speak('At your service!')
            webbrowser.open("google.com")


        elif "restart" in query:

            subprocess.call(["shutdown", "/r"])
            time.sleep(10) 
        

        elif "hibernate" in query or "sleep" in query:

            speak("Hibernating")
            subprocess.call("shutdown / h")
            time.sleep(5)

        
        elif "shutdown" in query or "turnoff" in query:

            speak("Shut down in process.")
            speak("You have 10 seconds to close and save everything.")
            subprocess.call("shutdown / s")
            time.sleep(10)

        
        elif "log off" in query or "sign out" in query:

            speak("Ok, your system will log off in 10 seconds make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
            time.sleep(5)


        elif "cpu status" in query or "cpu temperature" in query:
            
            cpu()


        elif "switch window" in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.keyUp('alt')


        elif "take a screenshot" in query or "screenshot this" in query:
       
            speak("What should I name the screenshot?")
            name = takeCommand().lower()
            speak("Please hold the screen")
            time.sleep(2)
            img=pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Done")


        elif 'time' in query:

            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        
        elif 'search for' in query:

            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            time.sleep(5)

        
        elif 'empty the recycle bin' in query:

            winshell.recycle_bin().empty(
                confirm = True, show_progress = False, sound = True
                )
            speak("Recycle Bin Recycled")

       
        elif "calculate" in query:
             
            app_id = "WVQW42-4XEJ25LEYJ"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)


        elif "what is" in query or "who is" in query:
             
            client = wolframalpha.Client("WVQW42-4XEJ25LEYJ")
            res = client.query(query)
             
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            
            except StopIteration:
                print ("No results")


        elif 'news' in query:
             
            try:
                
                jsonObj = urlopen(
                    'https://newsapi.org/v2/top-headlines?country=in&apiKey=81d89036c7f644cc90afa75866b7ee7c'
                    )
                data = json.load(jsonObj)
                i = 1
                 
                speak('Here are some top Headlines from the times of india')
                print('''=============== TIMES OF INDIA ============'''+ '\n')
                 
                for item in data['articles']:
                     
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
                
            except Exception as e:
                 
                print(str(e))


        elif "toss a coin" in query or "flip a coin" in query or "toss" in query:
                
            moves=["head", "tails"]
            cmove=random.choice(moves)
            speak("It's " + cmove)


        elif "don't listen" in query or "stop listening" in query:

            speak("for how long do you not want me to listen?")
            a = int(takeCommand())
            time.sleep(a)
            print(a)


        elif "bye" in query or "see ya later" in query or "stop" in query:

            speak('Leafy, Signing out!')
            print('Leafy, Signing out!')
            break

# create root window
root = Tk()

# root window title and dimension
root.title("Leafy")

# frame inside root window
frame = Frame(root)

img = Image.open("D:\Leafy\kindpng_1259258.png")
# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(img)

# Create a Label Widget to display the text or Image
label = Label(frame, image = img)

btnin = Button(frame, text = 'Click me!',
                command = leafy)

#Button to destroy the window
btnex = Button(frame, text = 'BYE',
                command = root.destroy)

frame.grid(columnspan=2, rowspan=2)
label.grid(column=0)
btnin.grid(column=0, row=0)
btnex.grid(column=0, row=1)

# all widgets will be here
# Execute Tkinter
root.mainloop()