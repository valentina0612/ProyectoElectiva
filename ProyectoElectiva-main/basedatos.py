import requests
import json

# Obtener datos de la API
peliResponse= requests.get("https://api.themoviedb.org/3/movie/550?api_key=&language=es-MX")
url = "https://api.themoviedb.org/3"


def ImprimirJson(peliJson):
    for key, value in peliJson.items():
        print(key, ":", value)


#Función para buscar una película por nombre
def buscarPeliculaNombre(nombre):
    peliResponse= requests.get(url+"/search/movie?api_key=&language=es-MX&query="+nombre+"&page=1")
    peliJson = json.loads(peliResponse.text)
    return peliJson

nombre = input("Ingrese el nombre de la película: ")
print(buscarPeliculaNombre(nombre)['results'][0]['overview'])
