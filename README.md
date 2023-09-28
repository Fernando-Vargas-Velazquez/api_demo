# Design Document: API REST CONTACTOS

## 1.- Descripciòn 
Ejeplo de una API REST para gestionar contactos en una BD utilizando FastAPI

## 2.- Objetivo
Realizar un ejemplo de diseño de una API REST de tipo CRUD y su posterior codificaciòn utilizando el framework [FastAPI] (https://fastapi.tiangolo.com/)

## 3.- Diseño de la BD
Para este ejemplo se utilizara el gestor de base de datos [SQLite] (https://www.sqlite.org/index.html) con las siguienres tablas:

### 3.1 Tabla: contactos
|No.|Campo|Tipo|Restricciones|Descripcion|
|--|--|--|--|--|
|1|id_contactos|int|PRIMARY key|Llave primaria de la tabla|
|2|nombre|varchar|100|Tipo texto|
|3|primer_apelLido|varchar|50|Tipo Texto|
|4|segundo_apellido|varchar|50|Tipo texto|
|5|email|varchar|50|Tipo Texto|
|6|telefono|varchar|13|Tipo Texto|

## 3.2 Script
'''sql
CREATE TABLE contactos (
    id_contacto INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    telefono VARCHAR(13) NOT NULL
);

## 4.1 Metodo POST
|No.|Propiedad|Detalle|
|--|--|--|
|1|Description|Endpoint para enviar datos a la API|
|2|Summary|Endpoint para enviar datos|
|3|Method|Post|
|4|Endpoint|http://localhost:8000/|
|5|QueryParam|NA(En general, los parametros de consulta no se utilizan en POST|
|6|PhatParam|NA(Los paht parametros, suelen estar en la URL y no en el cuerpo)|
|7|Data|Datos que se enviaran al servidor en el cuerpo de la solicitud|
|8|Versiones|V1|
|9|Status Code|201 create(el codigo de estado comunmente utilizados para POST)|
|10|Response-Type|application/json|
|11|Response|{"version":"V1","message":"Datos_recividos_correctamente","datatime":"25/09/23 9:52"}|
|12|Curl|curl-X'post''http://localhost:8000/'-H accept:application/json' '{"data":"ejemplo"}'|
|13|Status code(error)|400 Bad Request(codigo de estado comun para errores de solicitud)|
|14|Response Type(error)|application/json|
|15|Response(error)|{"error":"Mensaje de error detallado"}|


## 4.2 Metodo PATCH
|No.|Propiedad|Detalle|
|--|--|--|
|1|Description|Endpoint para realizar modificaciones parciales en un recurso de la API|
|2|Summary|Endpoint para modificar datos de forma parcial|
|3|Method|PATCH|
|4|Endpoint|http://localhost:8000/contactos/{id}|
|5|QueryParam|NA(En general, los parametros de consulta no se utilizan en PATCH)|
|6|PhatParam|{id}-Identificador del recurso que se modifica|
|7|Data|Datos parciales que se enviaran al servidor de la solicitud para modificar|
|8|Versiones|V1|
|9|Status Code|200 OK(El codidgo de estado comunmente utilizado para PATCH exitosos)|
|10|Response-Type|application/json|
|11|Response|{"version":"V1","message":"Recurso_modificado","datatime":"25/09/23 9:52"}|
|12|Curl|curl-X'PATCH''http://localhost:8000/contactos/{id}'-H 'accept:application/json' '{"data_parcial":"nuevo_valor"}'|
|13|Status code(error)|404 Not Found(codidgo de estado comun para los recursos que no se encuentran)|
|14|Response Type(error)|application/json|
|15|Response(error)|{"error":"Recurso_no_encontrados"}|

## 4.3 Metodo DELETE
|No.|Propiedad|Detalle|
|--|--|--|
|1|Description|Endpoint para eliminar recursos de la API|
|2|Summary|Endpoint para eliminar recursos|
|3|Method|Delete|
|4|Endpoint|http://localhost:8000/contactos/{id_contacto}|
|5|QueryParam|NA(En general,parametros de consulta no se utiliza en DELETE)|
|6|PhatParam|{id}-Identificador de los recursos a eliminar|
|7|Data|NA(no se envian datos en el cuerpo de una solicitud del DELETE)|
|8|Versiones|V1|
|9|Status Code|204 No content(utiliza para delete exitoso sin respuesta)|
|10|Response-Type|NA(No se espera la respuesta con contenido)|
|11|Response|NA(No hay cuerpo en la respuesta)|
|12|Curl|curl-X'Delete''http://localhost:8000/contactos/{id_contacto}'-H 'accept:application/json'|
|13|Status code(error)|404 Not Found(para recursos no encontrados)|
|14|Response Type(error)|application/json|
|15|Response(error)|{"error":"Recurso_no_encontrados"}|

## 4.4 Metodo PUT
|No.|Propiedad|Detalle|
|--|--|--|
|1|Description|Endpoint para actualizar de la API|
|2|Summary|Endpoint para actualizar recursos|
|3|Method|PUT|
|4|Endpoint|http://localhost:8000/contactos/{id_contacto}|
|5|QueryParam|NA(parametros de consulta no se ocupan en PUT)|
|6|PhatParam|{id}-Identificador de los recursos actualizados|
|7|Data|Datos actualizados se envian al servidor en el cuerpo de la solicitud|
|8|Versiones|V1|
|9|Status Code|200 OK(utilizado para Put exitoso)|
|10|Response-Type|application/json|
|11|Response|{"version":"V1","message":"Recurso_actualizado","datatime":"25/09/23 9:52"}|
|12|Curl|curl-X'Put''http://localhost:8000/contactos/{id_contacto}'-H 'accept:application/json'|
|13|Status code(error)|404(Not found)(codigo de estado comun para recursos no encontrados)|
|14|Response Type(error)|application/json|
|15|Response(error)|{"error":"Recurso_no_encontrados"}|

