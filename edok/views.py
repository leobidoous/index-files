from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


@permission_classes((IsAuthenticated,))
def search_document(request):
    url = 'https://intcare.edok.com.br/api/DocView.php?'
    url += 'k=' + settings.EDOK_API_KEY

    return render(request, "edok/search_document.html", locals())
