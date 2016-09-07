from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import filters

from .models import User
from .serializers import UserSerializer



# Viewsets define the behavior of the view
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username','is_player', 'first_name','last_name','email',)

    
