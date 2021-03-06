from rest_framework import viewsets, response, status
from .serializers import CitySerializer
from .models import City


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    cache_dict = {}
    cache_list = []

    def cache_response(self, name):
        try:
            print('Есть', self.cache_dict[name])   # проверяем наличие запроса в кэше
            return True
        except:
            self.cache_dict[name] = None   # добавляем значение в словарь "O(1)"
            self.cache_list.append(name)   # добавляем значение в конец списока "O(1)"
            if len(self.cache_list) > 100:   # проверяем длину списка "O(1)"
                self.cache_dict.pop(self.cache_list[0])  # Удаляем из словаря "O(1)"
                self.cache_list.pop(0)   # Если кеш больше 100, удаляем первый элемент "O(1)"
            return False

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        if self.cache_response(name):
            # print('Есть в кэше')
            return response.Response('true')   # Если есть в кэше, отвечаем "True"

        else:
            # print('Нет в кэше')
            if City.objects.filter(name=name).exists():   # Вв кэше нет, проверяем наличие в базе. Если нет, добавляем
                # print('Находится в бд')
                return response.Response('true')
            else:
                # print('Запись в бд')
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                # return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                return response.Response('false', status=status.HTTP_201_CREATED, headers=headers)



