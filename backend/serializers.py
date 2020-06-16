from rest_framework import serializers
from backend.models import Owner, Event


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = (
            'id', 'external_id', 'name', 'owner_type',
            'origin', 'active', 'created', 'last_modified'
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id', 'owner', 'external_id', 'name', 'description', 'start_time',
            'end_time', 'place_latitude', 'place_longitude', 'place_city',
            'place_state', 'place_country', 'place_address', 'place_name',
            'status', 'origin', 'is_page_owned', 'attending_count',
            'interested_count', 'cover_image_url', 'active', 'created',
            'last_modified'
        )
