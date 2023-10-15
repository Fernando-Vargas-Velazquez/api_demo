import requests
import json

URI = "https://www.dnd5eapi.co/api/classes"

response = requests.get(URI)

response_json = json.loads(response.text)

contador = 0

for resultado in response_json['results']:
    contador = contador + 1
    print(contador, ".", resultado['name'])

numero_personaje = int(input("Ingresa el número del personaje que deseas consultar: ")) - 1

if(numero_personaje >12):

    personaje_uri = response_json['results'][numero_personaje]['url']

    personaje_response = requests.get(f"https://www.dnd5eapi.co{personaje_uri}")
    personaje_json = json.loads(personaje_response.text)

    print(f"\nProficiencies de {personaje_json['name']}:")

    for proficiency in personaje_json['proficiencies']:
        print(proficiency['name'])

