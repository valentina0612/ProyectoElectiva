import datetime
#Librerías para el asistente
import speech_recognition as sr
import pyttsx3
import wikipedia
import subprocess as sub
from deep_translator import GoogleTranslator
import os
import time
import openai

#Conexion con la API de OpenAI
openai.api_key = "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"
name = "bolt"
#Para que el asistente te escuche
entrada = sr.Recognizer()
#Para que el asistente te hable
bot = pyttsx3.init()


#Voz del asistente en español
voz = bot.getProperty('voices')
bot.setProperty('voice',voz[0].id)

#Lista de sitios web
sitios = {  
        'google': 'google.com',
        'amazon': 'https://www.amazon.com/books',
        'youtube': 'https://www.youtube.com/',
        }   

print("Asistente virtual")
bot.say("Hola, soy tu asistente virtual")

#Función para que el asistente te hable
def hablar(texto):
    bot.say(texto)
    bot.runAndWait()

#Función para que el asistente te escuche
def escuchar():
    #Comprueba que el micrófono esté conectado
    try:
        #Escucha lo que dices y lo guarda
        with sr.Microphone() as source:
            print("Diga algo: ")
            audio = entrada.listen(source)
            bot.runAndWait()
            print("Reconociendo...")
            text = entrada.recognize_google(audio, language='es-ES')
            text = text.lower()
            if name in text:
                text = text.replace(name, '')
            if text == '':
                text = 'salir'
    except:
        text = 'salir' # Si hay algún error, se sale del programa
    return text


#Función para ejecutar el asistente
def ejecutarBot():
    #Mientras el asistente esté activo, podrás pedirle que haga cosas
    while True:
        bot.runAndWait()
        accion = escuchar()
        conversation = "\nUsuario: " + accion + "\nBolt: "
        print("Usuario: " + accion)

        #Si dices "salir" el asistente se desactiva
        if 'salir' in accion:
            hablar("Espero haberte ayudado, hasta luego")
            break
        
        #Si dices "abrir" el asistente te abre el sitio web que le digas (si está en la lista)
        elif 'abrir' in accion:
            for sitio in sitios:
                if sitio in accion:
                    sub.call(f'start chrome.exe {sitios[sitio]}', shell=True)
                    hablar(f'Abriendo {sitio}')
                    respuesta = f'Abriendo {sitio}'
                    conversation += respuesta
        
                    
        #Si dices "definir" el asistente te define lo que le digas en wikipedia
        elif 'definir' in accion:
            accion = accion.replace('definir', '')
            result = wikipedia.summary(accion, sentences=2)
            texto = str(result)
            traductor = GoogleTranslator(source='en', target='es')
            traduccion = traductor.translate(texto)
            respuesta = traduccion
            conversation += respuesta
            hablar(traduccion)
            
        #Si dices "reproducir" el asistente te reproduce en youtube lo que le digas
        elif 'reproducir' in accion:
            accion = accion.replace('reproducir', '')
            hablar(f'Reproduciendo {accion}')
            respuesta = f'Reproduciendo {accion}'
            conversation += respuesta
            accion = accion.replace(' ', '+')
            os.system(f'start chrome.exe https://www.youtube.com/results?search_query={accion}')
        
        #Si dices "buscar" el asistente te busca en google lo que le digas
        elif 'buscar' in accion:
            accion = accion.replace('buscar', '')
            hablar(f'Buscando {accion}')
            conversation += f'Buscando {accion}'
            accion = accion.replace(' ', '+')
            os.system(f'start chrome.exe https://www.google.com/search?q={accion}')
        
        #Si dices "comprar" el asistente te busca en amazon lo que le digas
        elif 'comprar' in accion:
            accion = accion.replace('comprar', '')
            hablar(f'Buscando {accion} en amazon')
            respuesta = f'Buscando {accion} en amazon'
            conversation += respuesta
            accion = accion.replace(' ', '+')
            os.system(f'start chrome.exe https://www.amazon.com/s?k={accion}')

        #Si dices "hora" el asistente te dice la hora
        elif 'hora' in accion:
            hora = datetime.datetime.now().strftime("%I:%M %p")
            hablar("La hora es: " + hora)
            respuesta = "La hora es: " + hora
            conversation += respuesta
        else:
            #Si el usuario no le da una orden especifica, el bot hablará con el usuario
            response = openai.Completion.create(
                engine="davinci",
                #El prompt es lo que el bot va a decir
                prompt=conversation,
                #La temperatura controla la creatividad del bot
                temperature=0.4,
                #max_tokens es la cantidad de palabras (máxima) que va a decir el bot
                max_tokens=150,
                #top_p es la probabilidad de que el bot diga una palabra
                top_p=1,
                #frequency_penalty controlan la repetición de palabras
                frequency_penalty=0,
                #presence_penalty verifica que el bot no diga palabras o frases irrelevantes
                presence_penalty=0.6,
                stop=["\n", " Usuario: ", " Bolt: "]
            )
            respuesta = response.choices[0].text
            hablar(respuesta)
            conversation += respuesta
        print("Bolt: " + respuesta+"\n")
    
        

if __name__ == "__main__":
    ejecutarBot()	