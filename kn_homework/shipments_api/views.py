from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.response import Response

from kn_homework.shipments_api.models import Shipment
from kn_homework.shipments_api.serializers import ShipmentSerializer


class ShipmentViewSet(viewsets.ViewSet):
    """
    API endpoint that allows shipments to be viewed or edited.
    """
    queryset = Shipment.objects.all().order_by('id')
    serializer_class = ShipmentSerializer

    def list(self, request):
        """
        List all Shipment instances
        """
        serializer = ShipmentSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a Shipment instance by ID
        """
        shipment = get_object_or_404(self.queryset, pk=pk)
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new `Shipment` instance
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return Response({
            'status': 'Invalid Input',
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def update(self, request, pk):
        """
        Update a `Shipment` instance
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            shipment = get_object_or_404(self.queryset, pk=pk)
            shipment.sender = serializer.validated_data['sender']
            shipment.receiver = serializer.validated_data['receiver']
            shipment.description = serializer.validated_data['description']
            shipment.tracking_code = serializer.validated_data['tracking_code']
            shipment.save()

            return Response({
                'status': 'Updated',
            }, status=status.HTTP_204_NO_CONTENT)

        return Response({
            'status': 'Invalid Input',
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, pk):
        """
        Delete a `Shipment` instance
        """
        shipment = get_object_or_404(self.queryset, pk=pk)
        shipment.delete()

        return Response({
            'status': 'Deleted',
        }, status=status.HTTP_204_NO_CONTENT)