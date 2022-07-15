from django.urls import path
from .views import *


urlpatterns = [
   path('', AdvertList.as_view()), 
   path('<int:pk>/', AdvertView.as_view(), name = 'advDetail'),
   path('add', AdvertCreate.as_view()),
   path('edit/<int:pk>', AdvertUpdate.as_view(), name = 'advEdit'),
   path('responses', ResponseList.as_view(), name = 'responses'),
   path('responses/accept/<int:pk>', ResponseAccept.as_view(), name = 'advAccept'),
   path('responses/delete/<int:pk>', ResponseDelete.as_view(), name = "advDelete"),
]