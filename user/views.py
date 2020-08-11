from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.pagination import DefaultResultsSetPagination
from user.serializers import UserSerializer
from .models import UserModel


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserModel.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = [IsAuthenticated]