from rest_framework import serializers 
from AirTrafficApp.models import Items

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['call_sign', 'aircraft_type', 'detail', 'origin', 'destination', 'action','time', 'timeliness', 'remarks']

        