from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import MeteoriteSerializer
from .models import Meteorite
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from tablib import Dataset
from .resources import MeteoriteResource
# Create your views here.
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def welcome(request):
    content = {"message": "Welcome to the Meteorites Landings API!"}
    return JsonResponse(content)

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_meteorites(request):
    user = request.user.id
    meteorites = Meteorite.objects.all()
    serializer = MeteoriteSerializer(meteorites, many=True)
    return JsonResponse({'meteorites': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_meteorite(request):
    payload = json.loads(request.body)
    user = request.user
    try:
        meteorite = Meteorite.objects.create(
            name=payload["name"],
            id=payload["id"],
            nametype=payload["nametype"],
            recclass=payload["recclass"],
            mass=payload["mass"],
            fall=payload["fall"],
            year=payload["year"],
            reclat=payload["reclat"],
            reclong=payload["reclong"],
            geoLocation=payload["geoLocation"]
        )
        serializer = MeteoriteSerializer(meteorite)
        return JsonResponse({'meteorites': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_meteorite(request, meteorite_id):
    user = request.user.id
    payload = json.loads(request.body)
    try:
        meteorite_item = Meteorite.objects.filter(id=meteorite_id)
        # returns 1 or 0
        meteorite_item.update(**payload)
        meteorite = Meteorite.objects.get(id=meteorite_id)
        serializer = MeteoriteSerializer(meteorite)
        return JsonResponse({'meteorite': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_meteorite(request, meteorite_id):
    user = request.user.id
    try:
        meteorite = Meteorite.objects.get(id=meteorite_id)
        meteorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        meteorite_resource = MeteoriteResource()
        dataset = meteorite_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response

    return render(request, 'export.html')

def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        meteorite_resource = MeteoriteResource()
        dataset = Dataset()
        new_meteorites = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(new_meteorites.read().decode('utf-8'),format='csv')
            result = meteorite_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            # Import now
            meteorite_resource.import_data(dataset, dry_run=False)

    return render(request, 'import.html')
