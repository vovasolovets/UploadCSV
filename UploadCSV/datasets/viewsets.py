from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .serializers import DataSetSerializer, GeneratorSerializer, DataSetExampleSerializer
from .models import DataSet, DataSetExample
from . import ProcessingStatus
from faker import Faker
from .tasks import generate_file


class DataSetViewSet(viewsets.ModelViewSet):
    serializer_class = DataSetSerializer
    queryset = DataSet.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=('post',), url_path='generate-file')
    def generate_file(self, request, pk=None, *args, **kwargs):
        fake = Faker()
        data_set = self.get_object()
        generator = GeneratorSerializer(request.POST or None)
        if generator.is_valid():
            example = DataSetExample.objects.create(data_set=data_set, file=fake.file_name(extension='csv'))
            generate_file.delay(example, generator.validated_data.get('row_number'))
            return Response('Your request is being processed')
        else:
            return Response(generator.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class DataSetExampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DataSetExampleSerializer
    queryset = DataSetExample.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=('get',), url_path='download-file')
    def download(self, request, pk=None, *args, **kwargs):
        example = self.get_object()
        if example.process_status == ProcessingStatus.READY:
            file_handle = example.file.open()

            # send file
            response = FileResponse(file_handle, content_type='whatever')
            response['Content-Length'] = example.file.size
            response['Content-Disposition'] = 'attachment; filename="%s"' % example.file.name

            return response
        return Response('Your file is not ready yet')
