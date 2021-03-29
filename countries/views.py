from django.shortcuts import render
from django.httpresponse import JsonRsponse
from rest_framework.parsers import JSONParser
from rest_framework import status


from countries.models import Countries
from countries.serializers import CountriesSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET','POST'])
def countries_list(request):
    if request.method == 'GET':
        countries = countries.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            countries = countries.filter(name__icontains=name)

        countries_serializer = countriesSerializer(countries, many=True)
        return JsonRsponse(countries_serializer.data, safe=False)

    elif request.method == 'POST':
        countries_data = JSONParser().parser(request)
        countries_serializer =CountriesSerializer(data=countries_data)
        if countries_serializer.is_valid():
            countries_serializer.save()
            return JsonResponse(countries_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(countries_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def countries_list(request, pk):
    try:
        countries = countries.objects.get(pk=pk)
    except countries.DoesNotExist:
        return JsonResponse({'message': 'The country does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        countries_serializer = countriesSerializer(countries)
        return JsonRsponse(countries_serializer.data)

    elif request.method == 'PuT':
        countries_data = JSONParser().parser(request)
        countries_serializer =CountriesSerializer(data=countries_data)
        if countries_serializer.is_valid():
            countries_serializer.save()
            return JsonResponse(countries_serializer.data)
        return JsonResponse(countries_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        countries.delete()
        return JsonResponse({'message': 'Country was deletd successfully!'}, status=status.HTTP_204_NO_CONTENT)