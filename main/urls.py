from django.urls import path
from . import views

# app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('index2', views.index2, name="index2"),
    path('predict', views.predict, name="predict"),
    path('about/', views.about, name="about"),
    path('howtouse/', views.howtouse, name="howtouse"),
    path('under_construction', views.under_construction, name="under_construction"),
    path('trainml/', views.trainml, name='trainml'),
    # path('upload/', views.upload, name='upload'),
]

urlpatterns += [

    path('upload/', views.upload, name='upload'),

]