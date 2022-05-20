from UploadCSV.celeryconfig import celery as main_app
from .models import DataSetExample
from . import FIELD_DICT, ProcessingStatus
from faker import Faker
import os
from django.conf import settings


def generate_data_type(faker, data_type):
    return getattr(faker, FIELD_DICT[data_type])()


@main_app.task
def generate_file(self, example_pk, n):
    example = DataSetExample.objects.filter(pk=example_pk).first()
    dataset = example.data_set
    faker = Faker()
    if dataset is None:
        return None
    fields_dict = {field['name']:[] for field in dataset.json_schema}
    for _ in range(n):
        for field in dataset.json_schema:
            print(field.keys())
            fields_dict[field['name']].append(generate_data_type(faker, field['data_type']))
    sorted_enum_list = sorted([(field['name'], field['order']) for field in dataset.json_schema], key=lambda x: x[1])
    sorted_list = [n[0] for n in sorted_enum_list]
    fields_file = ','.join([field for field in sorted_list])+'\n'
    for i in range(n):
        new_str = ','.join([fields_dict[field][i] for field in sorted_list])
        fields_file += new_str + '\n'
    print(fields_file, file=open(os.path.join(settings.MEDIA_ROOT, example.file.name), 'w'))
    example.process_status = ProcessingStatus.READY
    example.save()