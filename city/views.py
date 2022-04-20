from rest_framework import viewsets, response
from .serializers import CitySerializer
from .models import City


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


    def list(self, request, *args, **kwargs):
        return response.Response(['false'])
