import requests
import json

# Obtener datos de la API
peliResponse= requests.get("https://api.themoviedb.org/3/movie/550?api_key=dc108e924f5f078bf1c3ccf424b5ec93&language=es-MX")
url = "https://api.themoviedb.org/3"


def ImprimirJson(peliJson):
    for key, value in peliJson.items():
        print(key, ":", value)


#Función para buscar una película por nombre
def buscarPeliculaNombre(nombre):
    peliResponse= requests.get(url+"/search/movie?api_key=dc108e924f5f078bf1c3ccf424b5ec93&language=es-MX&query="+nombre+"&page=1")
    peliJson = json.loads(peliResponse.text)
    return peliJson

nombre = input("Ingrese el nombre de la película: ")
print(buscarPeliculaNombre(nombre)['results'][0]['overview'])
