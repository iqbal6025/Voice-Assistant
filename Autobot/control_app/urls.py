from django.urls import path
from . import views
urlpatterns = [
    path('',views.main),
    path('start/',views.speech_to_text)
]