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
                'enum': ['full_name', 'job', 'email', 'domain_name', 'phone_number',
                         'company_name', 'text', 'integer', 'address', 'date']
            },
            'min_value': {
                'type': 'integer',
            },
            'max_value': {
                'type': 'integer',
            },
            'order':{
                'type': 'integer'
            }
        }
    }
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
