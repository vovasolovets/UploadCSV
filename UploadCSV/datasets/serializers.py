from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
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
        return value


class GeneratorSerializer(serializers.Serializer):
    row_number = serializers.IntegerField()




class DataSetExampleSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'data_set_pk': 'data_set__pk',
    }

    class Meta:
        model = DataSetExample
        fields = ['file', 'process_status']

