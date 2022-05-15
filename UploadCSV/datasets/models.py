from django.db import models
from . import ProcessingStatus


class DataSet(models.Model):
    name = models.CharField(max_length=255)
    json_schema = models.JSONField()


class DataSetExample(models.Model):
    process_status = models.CharField(max_length=20,
                                      choices=ProcessingStatus.CHOICES,
                                      default=ProcessingStatus.PROCESSING)
    data_set = models.ForeignKey(DataSet, on_delete=models.CASCADE)
    file = models.FileField()
