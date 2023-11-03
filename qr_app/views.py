from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
import qrcode
from qr_app.models import QRCode
from PIL import Image
from io import BytesIO

# funcion encargada de generar el codigo QR 
def generate_qr(request):
    
    # si la peticion es tipo 'POST' entonces se genera el codigo QR
    if request.method == 'POST':
        
        # se obtiene el texto del formulario
        text = request.POST['text']
        
        # se crea un objeto QRCode
        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRRECT_L,
            box_size = 10,
            border = 4,            
        )
        # se agrega el texto al objeto  QRCode
        qr.add_data(text)
        
        # se genera el código QR
        qr.make(fit=True)
        
        # se crea una imagen a partir del codigo QR
        img = qr.make_make(fill_color='black', back_color='white')
        
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
        return redirect ('show_qr', qr_id=qr_code.id)
    
    # si la peticion no es de tipo POST, entonces se la pagina de generacion de codigos QR
    return render(request,'qr_app/generate_qr.html')

# funcion encargada de mostrar un codigo QR a partir de su ID
def show_qr(request, qr_id):
    # se obtiene el codigo QR de la base de datos
    qr_code =  QRCode.objects.get(id=qr_id)
    
    # se devuelve la pagina de visualizacion del codigo QR  con el codigo QR cargado
    return render(request, 'qr_app/show_qr.html', {'qr_code': qr_code})