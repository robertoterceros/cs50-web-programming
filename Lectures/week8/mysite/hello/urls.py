from django.urls import path
from . import views


#  Asociar una url con una vista y la forma en que django lo hace es con una lista
urlpatterns = [
    path("", views.index)

]
