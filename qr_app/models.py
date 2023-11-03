from django.db import models

class QRCode(models.Model):
    text = models.TextField()
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    
    def __str__(self):
        return self.text