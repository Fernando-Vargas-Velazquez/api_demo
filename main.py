from fastapi import FastAPI
import csv

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/v1/contactos")
async def get_contactos():
    # Define la ruta de tu archivo CSV
    csv_file_path = "contactos.csv"

    # Inicializa una lista para almacenar los datos de contacto
    contactos = []

    # Lee los datos del archivo CSV e imprímelos
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contactos.append(row)
            print(row)  # Imprime cada fila

    return {"contactos": contactos}
