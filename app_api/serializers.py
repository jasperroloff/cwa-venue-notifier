from django.core.validators import URLValidator
from rest_framework import serializers

from location.models import Location, PayloadDecodeError


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['url', 'description', 'address', 'uuid']
        read_only_fields = ['description', 'address', 'uuid']
        extra_kwargs = {
            'url': {'validators': [URLValidator]},
        }

    def create(self, validated_data):
        location = Location.get_by_url(validated_data['url'])
        location.save()
        return location

    def validate_url(self, url):
        try:
            Location.get_payload_from_url(url)
        except PayloadDecodeError:
            raise serializers.ValidationError("Error while decoding payload")

        return url
