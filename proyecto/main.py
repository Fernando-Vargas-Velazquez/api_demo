from fastapi import FastAPI, File, UploadFile, Query, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import csv
from PIL import Image
import os
from fastapi.staticfiles import StaticFiles
from PIL import ImageOps
import qrcode
import cv2
from pyzbar.pyzbar import decode

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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
    return {"message": "Hola mundo"}

class Contacto(BaseModel):
    id_contacto: int
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    email: str
    telefono: str

def leer_contactos():
    with open('contactos.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]

def escribir_contactos(contactos):
    with open('contactos.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=contactos[0].keys())
        writer.writeheader()
        writer.writerows(contactos)

@app.get('/contactos',
    description="Obtener todos los contactos",
    summary="Obtener contactos",
    status_code=status.HTTP_200_OK)
def obtener_contactos():
    """
    #Obtener todos los contactos
        ##Status code
        *200 OK
    """
    contactos = leer_contactos()
    return JSONResponse(content=contactos)

@app.post('/contactos',
    description="Agregar un nuevo contacto",
    summary="Agregar contacto",
    status_code=status.HTTP_201_CREATED)
def agregar_contacto(contacto: Contacto):
    """
    #Agregar un nuevo contacto
        ##Status code
        *201 Created
    """
    contactos = leer_contactos()
    contactos.append(contacto.dict())
    escribir_contactos(contactos)
    return JSONResponse(content=contacto.dict(), status_code=201)

@app.put('/contactos/{id_contacto}',
    description="Actualizar un contacto por su id_contacto",
    summary="Actualizar contacto",
    status_code=status.HTTP_200_OK)
@app.patch('/contactos/{id_contacto}',
    status_code=status.HTTP_200_OK)
def actualizar_contacto(id_contacto: int, contacto: Contacto):
    """
    #Actualizar un contacto por su id_contacto
        ##Status codes
        *200 OK
        *404 Not Found
    """
    contactos = leer_contactos()
    for idx, c in enumerate(contactos):
        if int(c['id_contacto']) == id_contacto:
            contactos[idx] = contacto.dict()
            escribir_contactos(contactos)
            return JSONResponse(content=contacto.dict())
    return JSONResponse(content={'mensaje': 'Contacto no encontrado'}, status_code=404)

@app.delete('/contactos/{id_contacto}',
    description="Borrar un contacto por su id_contacto",
    summary="Borrar contacto",
    status_code=status.HTTP_200_OK)
def borrar_contacto(id_contacto: int):
    """
    #Borrar un contacto por su id_contacto
        ##Status codes
        *200 OK
        *404 Not Found
    """
    contactos = leer_contactos()
    for idx, c in enumerate(contactos):
        if int(c['id_contacto']) == id_contacto:
            del contactos[idx]
            escribir_contactos(contactos)
            return JSONResponse(content={'mensaje': 'Contacto borrado'})
    return JSONResponse(content={'mensaje': 'Contacto no encontrado'}, status_code=404)

@app.get('/contactos/buscar',
    description="Buscar contactos por nombre",
    summary="Buscar contactos por nombre",
    status_code=status.HTTP_200_OK)
def buscar_por_nombre(nombre: str = Query(...)):
    """
    #Buscar contactos por nombre
        ##Status code
        *200 OK
    """
    contactos = leer_contactos()
    resultados = [c for c in contactos if nombre.lower() in c['nombre'].lower()]
    return JSONResponse(content=resultados)

IMAGES_DIRECTORY = 'static'
os.makedirs(IMAGES_DIRECTORY, exist_ok=True)

@app.post('/imagenes',
    description="Subir y editar imágenes",
    summary="Subir imágenes",
    status_code=status.HTTP_200_OK)
def subir_imagen(
    imagen: UploadFile = File(...),
    crop: str = None,
    fliph: bool = False,
    colorize: bool = False
):
    """
    #Subir y editar imágenes
        ##Status code
        *200 OK
    """
    nombre_archivo = os.path.join(IMAGES_DIRECTORY, imagen.filename)
    with open(nombre_archivo, 'wb') as buffer:
        buffer.write(imagen.file.read())

    if crop:
        left, top, right, bottom = map(int, crop.split(','))
        img = Image.open(nombre_archivo)
        img = img.crop((left, top, right, bottom))
        img.save(nombre_archivo)
    
    if fliph:
        img = Image.open(nombre_archivo)
        img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        img.save(nombre_archivo)
    
    if colorize:
        img = Image.open(nombre_archivo)
        img = img.convert("L")
        img = ImageOps.colorize(img, '#ff0000', '#0000ff')
        img = img.convert("RGB")
        img.save(nombre_archivo)

    return JSONResponse(content={'mensaje': 'Imagen procesada y guardada', 'ruta' : 'https://8000-fernandovargasv-apidemo-j3n8e2m2yyu.ws-us105.gitpod.io/' + nombre_archivo})


@app.get('/generar_qr/{id_contacto}',
    description="Generar un código QR para un contacto por su id_contacto",
    summary="Generar QR por ID",
    status_code=status.HTTP_200_OK)
def generar_qr_por_id(id_contacto: int):
    """
    #Generar un código QR para un contacto por su id_contacto
        ##Status codes
        *200 OK
        *404 Not Found
    """
    contactos = leer_contactos()
    for c in contactos:
        if int(c['id_contacto']) == id_contacto:
            datos_contacto = f"Id del contacto: {c['id_contacto']}, " \
                             f"Nombre: {c['nombre']}, " \
                             f"Primer Apellido: {c['primer_apellido']}, " \
                             f"Segundo Apellido: {c['segundo_apellido']}, " \
                             f"Telefono: {c['telefono']}, " \
                             f"Email: {c['email']} "

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(datos_contacto)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"static/codigo_qr_{id_contacto}.png")

            return JSONResponse(content={
                'mensaje': f'QR de contacto {id_contacto} creado',
                'ruta': f'https://8000-fernandovargasv-apidemo-j3n8e2m2yyu.ws-us105.gitpod.io/static/codigo_qr_{id_contacto}.png'
            })

    return JSONResponse(content={'mensaje': f'El contacto con id: {id_contacto} no fue encontrado'}, status_code=404)

class Imagen(BaseModel):
    imagen: UploadFile

@app.post('/leer_qr/',
    description="Leer el código QR de una imagen",
    summary="Leer código QR",
    status_code=status.HTTP_200_OK)
def leer_qr_del_contacto(imagen: UploadFile):
    try:
        with open('temp.png', 'wb') as temp:
            temp.write(imagen.file.read())

        imagen_cv2 = cv2.imread('temp.png', 0)
        qr_codes = decode(imagen_cv2)

        if not qr_codes:
            return JSONResponse(content={'mensaje': 'No se encontró ningún código QR en la imagen'}, status_code=400)

        datos_qr = qr_codes[0].data.decode('utf-8')
        return JSONResponse(content={'mensaje': 'Datos del código QR', 'datos': datos_qr})

    except Exception as e:
        return HTTPException(detail=str(e), status_code=500)

    finally:
        os.remove('temp.png')
