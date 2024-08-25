from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core.views import *

app_name = 'core'

urlpatterns = [ 
    path('contact/', ContactView.as_view(), name="core-contact"),
    path('deal/', DealView.as_view(), name="core-deal"),
    path('associate/', AssociateView.as_view(), name="core-associate"),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)