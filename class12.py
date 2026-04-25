import pyttsx3
import speech_recognition as sr
import threading
import pywhatkit
import queue
import datetime
import wikipedia
import random
import time

reminder_list = []

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.45)

listener = sr.Recognizer()
speech_queue = queue.Queue()

def talk(speech_text):
    print(f"Assistant: {speech_text}")

    def text_to_speech():
        engine.say(speech_text)
        engine.runAndWait()
        engine.stop()
        
    threading.Thread(target = text_to_speech, daemon = True).start()

def voice_input():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            print(f"User: {command}")
            return command
        
    except:
        command = ""

    return command

def reminder_check():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminder_list:
            if current_time == reminder['time']:
                talk(f"Remember to {reminder['task']} soon.")
                reminder_list.remove(reminder)
        time.sleep(30)
    
threading.Thread(target = reminder_check, daemon = True).start()
    
def run_assistant():
    talk("Hello, how are you today?")

    while True:
        voice_command = voice_input()

        if voice_command == "":
            continue
        
        if "date" in voice_command:
            date_now = datetime.datetime.now().strftime("%A, %B %d, %Y")    #A = day (Monday), B = Month, d = date (08), Y = year
            talk(f"The date today is {date_now}")
            
        elif "time" in voice_command:
            time_now = datetime.datetime.now().strftime("%I:%M %p")     #I:M = time (10:58), p = AM/PM
            talk(f"The time is {time_now}")

        elif "wikipedia" in voice_command:
            wiki_topic = voice_command.replace("wikipedia", " ").strip()

            try:
                info = wikipedia.summary(wiki_topic, sentences = 2)
                talk(info)

            except:
                talk("Sorry, I could not find that on Wikipedia.")
        
        elif "joke" in voice_command:
            joke = [
                "What’s the smartest insect? A spelling bee!", "What does a storm cloud wear under his raincoat? Thunderwear.", "What do you call an ant who fights crime? A vigilANTe!"
            ]
            talk(random.choice(joke))

        elif "remind me to" in voice_command:
            try:
                reminder_topic = voice_command.replace("remind me to", "")

                if "at" in reminder_topic:    #Call mom at 5 PM
                    task, reminder_time = reminder_topic.split("at")
                    task = task.split()
                    reminder_time = reminder_time.split()
                    reminder_list.append({'task': task, 'time': reminder_time})
                    talk(f"Reminder set for {task} at {reminder_time}")

                else:
                    talk("Please specify the time you'd like to be reminded of your task.")

            except:
                talk("Sorry, I could not set the reminder.")

        elif "reminders" in voice_command:
            talk("Your reminders are:")
            for i in reminder_list:
                talk(i)

        elif "exit" in voice_command or "stop" in voice_command or "bye" in voice_command:
            talk("Goodbye, have a great day.")
            break

run_assistant()