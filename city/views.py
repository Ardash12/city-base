from rest_framework import viewsets, response, status
from .serializers import CitySerializer
from .models import City


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def create(self, request, *args, **kwargs):
        if City.objects.filter(name=request.data['name']).exists():
            return response.Response(['true'])
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            # return response.Response(['false'])
            # return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return response.Response('false', status=status.HTTP_201_CREATED, headers=headers)

