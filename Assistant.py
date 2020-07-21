import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import sys
import random
import requests
import json

engine = pyttsx3.init('sapi5')  # taking voices from sapi5 which is windows api for voice
voices = engine.getProperty('voices')
# print(voices)  # We get two voice male and female
# print(voices[0].id) #DAVID male voice
# print(voices[1].id) #ZIRA male voice

engine.setProperty('voices', voices[1].id)


def speak(audio):
    """ function used for speaking"""
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    """ Wishes based on Time"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Jarvis sir. Please tell me how may I help you")


def takecommand():
    """It take microphone input from users and return string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # seconds of non speaking phase
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Using google speech Recognition API
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")

        return "None"  # str Not original None
    return query


if __name__ == '__main__':
    wishMe()

    while True:
        query = takecommand().lower()
        # print(query)

        # Logic for Executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', "")
            # print(query)
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")

        elif 'open gmail' in query:
            webbrowser.open('https://mail.google.com/mail/u/0/')

        elif 'open whatsapp' in query:
            webbrowser.open('https://web.whatsapp.com/')

        elif 'play some music' in query:
            music_dir = "D:\\Music"
            songs = os.listdir(music_dir)
            rand = random.randint(0, len(songs))
            os.startfile(os.path.join(music_dir, songs[rand]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, The Time is {strTime}")

        elif "today's news" in query:
            speak("Todays Top Headlines from various Sources...")

            url = os.environ.get("News_Api")
            news = requests.get(url).text

            news_dict = json.loads(news)
            articles = news_dict["articles"]
            lenght = len(articles)
            for index, art in enumerate(articles, 1):
                speak(art['title'])
                if index != lenght:
                    speak("Next News...")
            speak("Thank You...")

        elif 'stop' in query:
            speak("Thank you Sir for giving your valuable Time")
            sys.exit()
