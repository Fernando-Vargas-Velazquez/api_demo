from fastapi import FastAPI, status
import csv

app = FastAPI()

@app.get("/", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint raiz de la Api Contactos",
    summary="Endpoint raiz")
async def root():
    """
    #Endpoint raiz
    ##Status code
    *201 created
    """
    return {"message": "Hello World"}

@app.get(
    "/v1/contactos", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint para listar contactos en la Api Contactos",
    summary="Endpoint para listar cotactos")
async def get_contactos():
    
    # Define la ruta de tu archivo CSV
    archivo_contactos = "contactos.csv"

    # Inicializa una lista para almacenar los datos de contacto
    contactos = []

    # Lee los datos del archivo CSV y los impríme
    with open(archivo_contactos, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contactos.append(row)
            print(row)  # Imprime cada fila

    return {"contactos": contactos}
