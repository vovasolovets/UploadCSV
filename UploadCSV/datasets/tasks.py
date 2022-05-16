from ..celeryconf import app as main_app
from .models import DataSet, DataSetExample
from . import FIELD_DICT, ProcessingStatus
from faker import Faker
import os
from django.conf import settings


def generate_data_type(faker, data_type):
    return getattr(faker, FIELD_DICT['data_type'])()


@main_app.task
def generate_file(self, example_pk, n):
    example = DataSetExample.objects.filter(pk=example_pk).first()
    dataset = example.dataset
    faker = Faker()
    if dataset is None:
        return None
    fields_dict = {field['name']:[] for field in dataset.json_schema}
    for _ in range(n):
        for field in dataset.json_schema:
            fields_dict[field['name']].append(generate_data_type(faker, field['data_type']))
    sorted_list = sorted([field['name'] for field in dataset.json_schema], key=lambda x: x.get('order', 9999))
    fields_file = ','.join(sorted([field['name'] for field in sorted_list]))+'\n'
    for i in range(n):
        new_str = ','.join([fields_dict[field][i] for field in sorted_list])
        fields_file += new_str + '\n'
    print(fields_file, file=open(os.path.join(settings.MEDIA_ROOT, example.file.name), 'w'))
    example.status = ProcessingStatus.READY
    example.save()