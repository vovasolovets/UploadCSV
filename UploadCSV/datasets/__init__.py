DATASET_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'fields': {
            'name': {
                'type': 'string',
                'required': True
                },
            'data_type': {
                'type': 'string',
                'enum': ['full_name', 'email', 'domain_name', 'phone_number',
                         'company_name',  'address', 'date'],
                'required': True
            },
            'order':{
                'type': 'integer',
                'required': True
            }
        }
    }
}


FIELD_DICT = {
    'full_name': 'name',
    'email': 'email',
    'domain_name': 'domain_name',
    'phone_number': 'phone_number',
    'company_name': 'company',
    'text': 'text',
    'integer': 'numerify',
    'address': 'address',
    'date': 'date',
}


class ProcessingStatus:
    PROCESSING = 'processing'
    READY = 'ready'
    ERROR = 'error'
    CHOICES = (
        (PROCESSING, 'processing'),
        (READY, 'ready'),
        (ERROR, 'error')
    )
