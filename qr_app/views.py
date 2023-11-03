from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
import qrcode
from qr_app.models import QRCode
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# funcion encargada de generar el codigo QR 
def generate_qr(request):
    
    # si la peticion es tipo 'POST' entonces se genera el codigo QR
    if request.method == 'POST':
        
        # se obtiene el texto del formulario
        text = request.POST['text']
        
        # se crea un objeto QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,            
        )
        # se agrega el texto al objeto  QRCode
        qr.add_data(text)
        
        # se genera el código QR
        qr.make(fit=True)
        
        # se crea una imagen a partir del codigo QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # se guarda el codigo QR en el modelo 'QRCode' de 'qr_app' y se crea un objeto QRCode con el texto recibido
        qr_code = QRCode(text=text)
        
        # se crea un buffer para almacenar la imagen del codigo QR
        buffer = BytesIO()
        
        # se guarda la imagen del codigo qr en el buffer 
        img.save(buffer, format='PNG')
        
        # se asigna la imagen del codigo QR al modelo 
        qr_code.qr_code_image.save(f'{text}.png', ContentFile(buffer.getvalue()))
        
        # se guarda el modelo en la base de datos
        qr_code.save()
        
        # se redirecciona a al vista de visualizacion del codigo QR 
        return redirect ('qr_app:show_qr', qr_id=qr_code.id)
    
    # si la peticion no es de tipo POST, entonces se la pagina de generacion de codigos QR
    return render(request,'qr_app/generate_qr.html')


# funcion encargada de mostrar un codigo QR a partir de su ID
def show_qr(request, qr_id):
    # se obtiene el codigo QR de la base de datos
    qr_code =  QRCode.objects.get(id=qr_id)
    
    # se devuelve la pagina de visualizacion del codigo QR  con el codigo QR cargado
    return render(request, 'qr_app/show_qr.html', {'qr_code': qr_code})


# vista encargada de mostrar la lista de todos lo QR generados
def qr_list(request):
    qr_codes = QRCode.objects.all()
    
    context = {
        'qr_codes':qr_codes,
    }
    
    return render(request,'qr_app/list_qr.html',context)



#vista encargada de generar un pdf de los códigos qr
def generate_pdf_catalog(request):
    # se obtiene la lista de codigos QR
    qr_codes = QRCode.objects.all()

    # se configura un buffer para almacenar el PDF
    buffer = BytesIO()

    # se crea el documento PDF
    c = canvas.Canvas(buffer, pagesize=letter)

    # se configura el tamaño y posición de las tarjetas de codigos QR
    card_width = 200
    card_height = 200
    margin = 20
    x = margin
    y = letter[1] - margin - card_height

    for qr_code in qr_codes:
        # dibuja la tarjeta del codigo QR en el PDF
        c.drawImage(qr_code.qr_code_image.path, x, y, card_width, card_height)
        
        # escribe el ID del codigo QR en la tarjeta
        c.drawString(x, y - 10, f"Código QR ID: {qr_code.id}")
        
        # se mueve el cursor a la siguiente tarjeta, evitando que se salga de los limites de la pagina
        x += card_width + margin
        if x + card_width + margin > letter[0]:
            x = margin
            y -= card_height + margin

    # se guarda el documento
    c.save()

    # se configura la respuesta para descargar el PDF.
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='catalogo_qr.pdf')

    # devuelve la respuesta
    return response