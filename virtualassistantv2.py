import os
import sys
import pyttsx3 as ts
import calendar
import time
import serial
import urllib3 
import requests
import smtplib
from weather import Weather,Unit
import speech_recognition as sr

#serial interface with arduino
#if your using arduino serial module uncomment below line 
#ardserial=serial.Serial('com9',9600)

#pyttsx3 module for text to speech conversion
def friday(audio):
    engine = ts.init()
    engine.say(audio)
    engine.runAndWait()

#to recognize the audio
def recognizeaudio():
    a=sr.Recognizer()
    with sr.Microphone() as source:
        print("say something")
        a.pause_threshold=1
        a.adjust_for_ambient_noise(source, duration=1)
        audio=a.listen(source)

#I used sphinx module for converting from speech to text (does not require internet)
#uncomment if you want to use google stt (requires internet)

    try:
        command=a.recognize_google(audio).lower()
        #command=a.recognize_sphinx(audio).lower()
        print("you said:" + command)

    except sr.UnknownValueError:
        print("friday couldn't hear you")
        command=recognizeaudio();

    return command

#for executing commands
def mycommand(command):
    if "hi friday" in command:
        friday("hello sir")
        friday("what can i do for you?")

    #command for system time
    elif "what is the time now" in command:
        friday(time.asctime())

        
    elif "how are you" in command:
        friday("I am great")
        friday("I hope you are also doing well sir")

    #command for shutdown     
    elif "shutdown" in command:
         friday("shuting down in")
         os.system("shutdown -s")

    elif "what is the weather today" in command:
         weather = Weather(unit=Unit.CELSIUS)
         location = weather.lookup_by_location('chennai')
         condition = location.condition
         friday(condition.text)
         friday(weather.text)

    #command for forecast
    elif "what will be the weather in coming days" in command:
        engine = ts.init()
        weather = Weather(unit=Unit.CELSIUS)
        engine.say("weather about upcoming days")
        location = weather.lookup_by_location('chennai')
        forecasts = location.forecast
        for forecast in forecasts:
            engine.say("it seems to be" + forecast.text)
            engine.say("on" + forecast.date)
            engine.say("high will be" + forecast.high + "degree celsius")
            engine.say("low will be" + forecast.low + "degree celsius")
            engine.runAndWait()

    #command for room temeprature
    #I used arduino for getting my room temperature from dht-11 sensor
    
    elif "what is my room temperature" in command:
        income = str(ardserial.readline()[0:-2])
        friday(income+"degree celsius")

    elif "friday you up" in command:
        friday("yes sir!")

    #command for restart
    elif "restart" in command:
        friday("Sure!")
        os.startfile("shutdown -r")

    #command for opening google
    elif "go to google" in command:
        os.startfile("https://www.google.co.in/")

    #command for opening email
    elif "send an email" in command: 
       friday("Who is the recipient?")
       recipient = recognizeaudio()
             
    #type your recipient name in quotes to whom you want to send
       if "spider" in recipient:
           
           friday('What should I say?')
           content = recognizeaudio()

            #init gmail SMTP
           mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
           mail.ehlo()

            #encrypt session
           mail.starttls()

            #Give your username and password to login 
           mail.login("xxxx","xxxx")

            #your recipient username and mail id
           mail.sendmail("xxx", "xxx", content)

            #end mail connection
           mail.close()

           friday("Email sent.")

        
              
    else:
        friday("I don't know what do you mean sir!")
        friday("try speaking correctly")
        
    
    
while True:
    mycommand(recognizeaudio())
