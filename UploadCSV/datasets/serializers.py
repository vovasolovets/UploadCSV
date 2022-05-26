from rest_framework import serializers
import jsonschema
from .models import DataSet, DataSetExample
from . import DATASET_SCHEMA


class GeneratorSerializer(serializers.Serializer):
    row_number = serializers.IntegerField()


class DataSetExampleSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'data_set_pk': 'data_set__pk',
    }

    link = serializers.SerializerMethodField(method_name='get_link')
    file_name = serializers.SerializerMethodField(method_name='get_file_name')

    def get_link(self, obj):
        return '/upload/datasets/%i/examples/%i/download-file' % (obj.data_set.id, obj.id)

    def get_file_name(self, obj):
        return obj.file.name

    class Meta:
        model = DataSetExample
        fields = ['file', 'process_status', 'link', 'file_name']


class JsonSchemaSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    data_type = serializers.ChoiceField(choices=[
        ('full_name', 'Full Name'),
        ('email', 'Email'),
        ('domain_name', 'Domain Name'),
        ('phone_number', 'Phone Number'),
        ('company_name', 'Company Name'),
        ('address', 'Address'),
        ('date', 'Date')], required=True)
    order = serializers.IntegerField(required=True)


class DataSetSerializer(serializers.ModelSerializer):
    datasetexample_set = DataSetExampleSerializer(many=True, read_only=True)
    # json_schema = JsonSchemaSerializer(many=True)


    class Meta:
        model = DataSet
        fields = ['name', 'json_schema', 'datasetexample_set', 'id']
        widgets = {}

    def validate_json_schema(self, value):
        try:
            jsonschema.validate(value, DATASET_SCHEMA)
        except jsonschema.ValidationError:
            raise serializers.ValidationError('Schema not valid')
        return value

