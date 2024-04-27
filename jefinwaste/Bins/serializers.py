# serializers.py
from rest_framework import serializers
from .models import Bin

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ['Bin_Id', 'bin_content']
