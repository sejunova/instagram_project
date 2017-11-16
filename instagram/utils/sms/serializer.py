import re
from rest_framework import serializers

class SMSSerializer(serializers.Serializer):
    receiver = serializers.CharField()
    message = serializers.CharField(max_length=90)

    def validate_receiver(self, value):
        pattern1 = re.compile(r'^(010)(\d{4})(\d{4})$')
        pattern2 = re.compile(r'^(01)[1-9](\d{3})(\d{4})$')

        if pattern1.match(value) or pattern2.match(value):
            return value
        else:
            raise serializers.ValidationError("Invalid phone number")


