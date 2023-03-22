import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
import subprocess as sub
from deep_translator import GoogleTranslator
import os

name = "bolt"
entrada = sr.Recognizer()
bot = pyttsx3.init()

voz = bot.getProperty('voices')
bot.setProperty('voice',voz[0].id)

sitios = {  
        'google': 'google.com',
        'amazon': 'https://www.amazon.com/books',
        'youtube': 'https://www.youtube.com/',
        }   

def hablar(texto):
    bot.say(texto)
    bot.runAndWait()
    
def escuchar():
    try:
        with sr.Microphone() as source:
            print("Diga algo: ")
            audio = entrada.listen(source)
            print("Reconociendo...")
            text = entrada.recognize_google(audio, language='es-ES')
            text = text.lower()
            if name in text:
                text = text.replace(name, '')
                print(text)
    except:
        pass
    return text 

def ejecutarBot():
    bot.say("Hola, soy tu asistente virtual")
    bot.runAndWait()
    accion = escuchar()
    if 'salir' in accion:
        hablar("Adios")
        exit()

    elif 'abrir' in accion:
        for sitio in sitios:
            if sitio in accion:
                sub.call(f'start chrome.exe {sitios[sitio]}', shell=True)
                hablar(f'Abriendo {sitio}')

    elif 'definicion' in accion:
        accion = accion.replace('buscar', '')
        result = wikipedia.summary(accion, sentences=2)
        texto = str(result)
        traductor = GoogleTranslator(source='en', target='es')
        traduccion = traductor.translate(texto)
        print(traduccion)
        hablar(traduccion)

    elif 'reproducir' in accion:
        accion = accion.replace('reproducir', '')
        hablar(f'Reproduciendo {accion}')
        accion = accion.replace(' ', '+')
        os.system(f'start chrome.exe https://www.youtube.com/results?search_query={accion}')
    
    elif 'buscar' in accion:
        accion = accion.replace('buscar', '')
        hablar(f'Buscando {accion}')
        accion = accion.replace(' ', '+')
        os.system(f'start chrome.exe https://www.google.com/search?q={accion}')
    
    elif 'comprar' in accion:
        accion = accion.replace('comprar', '')
        hablar(f'Buscando {accion} en amazon')
        accion = accion.replace(' ', '+')
        os.system(f'start chrome.exe https://www.amazon.com/s?k={accion}')

    elif 'hora' in accion:
        hora = datetime.datetime.now().strftime("%I:%M %p")
        hablar("La hora es: " + hora)
    else:
        hablar(accion)

if __name__ == "__main__":
    ejecutarBot()	