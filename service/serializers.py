from rest_framework import serializers


class ListItemIDSerializer(serializers.Serializer):
    item_ids = serializers.ListField(required=True, child=serializers.IntegerField(required=True))

    class Meta:
        fields = '__all__'
