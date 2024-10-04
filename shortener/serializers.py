from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('original_url',)

    # Optionally, you can override the create method if needed (for additional logic)
    def create(self, validated_data):
        # The short_code will automatically be generated in the model's save() method
        return URL.objects.create(**validated_data)
# ============================================================================
# from rest_framework import serializers
# from .models import URL

# class URLSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = URL
#         fields = ['original_url', 'short_code']
