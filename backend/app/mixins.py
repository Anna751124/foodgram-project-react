from rest_framework import mixins, viewsets

class ListCreateDelViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass