from rest_framework import serializers
import jsonschema
from .models import DataSet, DataSetExample
from . import DATASET_SCHEMA


class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ['name', 'json_schema']

    def validate_json_schema(self, value):
        try:
            jsonschema.validate(value, DATASET_SCHEMA)
        except jsonschema.ValidationError:
            raise serializers.ValidationError('Schema not valid')


class GeneratorSerializer(serializers.Serializer):
    row_number = serializers.IntegerField()


class DataSetExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetExample
        fields = ['file', 'status']

