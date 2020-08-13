from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Actor
from .serializers import ActorListSerializer, ActorDetailSerializer
from .service import ModelViewSetPermission

class ActorViewSet(viewsets.ViewSet):
    '''Вывод списка актеров и актера по айди'''
    def list(self, request):
        queryset = Actor.objects.all()
        serializer = ActorListSerializer(queryset, many = True)
        return Response(data = serializer.data)

    def retrieve(self, request, pk = None):
        queryset = Actor.objects.all()
        actor = get_object_or_404(queryset, pk = pk)
        serializer = ActorDetailSerializer(actor)
        return Response(data = serializer.data)

class ActorReadOnly(viewsets.ReadOnlyModelViewSet):
    '''Вывод списка актеров и актера по айди'''
    queryset = Actor.objects.all()
    serializer_class =  ActorDetailSerializer

class ActorModelViewSet(ModelViewSetPermission):
    '''Все, чот связано актерами'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    permission_classes = [permissions.IsAdminUser]
    permission_classes_by_action = {
        'get': [permissions.AllowAny],
        'update': [permissions.IsAuthenticated]
    }

    # @action(detail = False, permission_classes = [permissions.IsAuthenticated])
    # def my_list(self, request, *args, **kwargs):
    #     reurn super().list(request, *args, **kwargs)

    @action(detail = True, methods = ['get', 'put'])#, renderer_classes = [renderers.AdminRenderer])
    def example(self, request, *args, **kwargs):
        actor = self.get_object()
        serializer = ActorDetailSerializer(actor)
        return Response(serializer.data)

    # def get_permission(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     elif self.action == 'example':
    #         permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]