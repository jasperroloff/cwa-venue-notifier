from django.urls import path
from django.views.generic import TemplateView

from app_web.views import UploadQRCodeView, LocationDetailView

urlpatterns = [
    path('', UploadQRCodeView.as_view(), name='index'),
    path('location/<uuid:uuid>', LocationDetailView.as_view(), name='location-details'),
    path('location/<path:url>', LocationDetailView.as_view(), name='location-details'),
    path('datenschutz/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('impressum/', TemplateView.as_view(template_name='imprint.html'), name='imprint'),
    path('scan/', TemplateView.as_view(template_name='scan.html'), name='scan'),
]
