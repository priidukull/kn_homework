from rest_framework import serializers

from kn_homework.shipments_api.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'sender', 'receiver', 'tracking_code', 'description']