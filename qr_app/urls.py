# qr_app/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'qr_app'
urlpatterns = [
    path('', views.generate_qr, name='generate_qr'),
    path('show/<int:qr_id>/', views.show_qr, name='show_qr'),
    path('qr_list', views.qr_list, name='qr_list'),
    path('generate_pdf_catalog/', views.generate_pdf_catalog, name='generate_pdf_catalog'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
