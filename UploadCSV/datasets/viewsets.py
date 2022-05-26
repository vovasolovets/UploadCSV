from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from .serializers import DataSetSerializer, GeneratorSerializer, DataSetExampleSerializer
from .models import DataSet, DataSetExample
from . import ProcessingStatus, DATASET_SCHEMA
from faker import Faker
from .tasks import generate_file


class DataSetViewSet(viewsets.ModelViewSet):
    default_serializer_class = DataSetSerializer
    queryset = DataSet.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # parser_classes = (FormParser,)
    serializers = {
        'generate-file': GeneratorSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.default_serializer_class)

    @action(detail=True, methods=('get', 'post'), url_path='generate-file')
    def generate_file(self, request, pk=None, *args, **kwargs):
        fake = Faker()
        data_set = self.get_object()
        generator = GeneratorSerializer(data=request.data or None)
        if generator.is_valid():
            example = DataSetExample.objects.create(data_set=data_set, file=fake.file_name(extension='csv'))
            generate_file.delay(example_pk=example.pk, n=generator.validated_data.get('row_number'))
            return Response('Your request is being processed')
        else:
            return Response(generator.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('get', ), url_path='get-schema')
    def get_schema(self, request):
        return Response(DATASET_SCHEMA)


class DataSetExampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DataSetExampleSerializer
    queryset = DataSetExample.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, client_pk=None, maildrop_pk=None):
        queryset = DataSetExample.objects.filter(mail_drop__client=client_pk, mail_drop=maildrop_pk)
        serializer = DataSetExampleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, data_set_pk=None):
        queryset = DataSetExample.objects.filter(pk=pk, data_set__pk=data_set_pk)
        example = get_object_or_404(queryset, pk=pk)
        serializer = DataSetExampleSerializer(example)
        return Response(serializer.data)

    @action(detail=True, methods=('get',), url_path='download-file')
    def download(self, request, pk=None,data_set_pk=None,  *args, **kwargs):
        queryset = DataSetExample.objects.filter(pk=pk, data_set__pk=data_set_pk)
        example = get_object_or_404(queryset, pk=pk)
        if example.process_status == ProcessingStatus.READY:
            file_handle = example.file.open()

            # send file
            response = FileResponse(file_handle, content_type='whatever')
            response['Content-Length'] = example.file.size
            response['Content-Disposition'] = 'attachment; filename="%s"' % example.file.name

            return response
        return Response('Your file is not ready yet')
