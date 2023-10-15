import qrcode

def generar_codigo_qr(datos_contacto):
    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agrega los datos de contacto al código QR
    qr.add_data(datos_contacto)
    qr.make(fit=True)

    # Crea una imagen
    img = qr.make_image(fill_color="black", back_color="white")

    # Guarda la imagen
    img.save("codigo_qr_contacto.png")

# Ejemplo de uso
datos_contacto = "Nombre: Juan Perez\nTelefono: 123456789\nEmail: juan@example.com"
generar_codigo_qr(datos_contacto)
