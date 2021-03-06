# DataObject and related objects


integer_data_object = {
    'type': 'integer',
    'value': 3
}

boolean_data_object = {
    'type': 'boolean',
    'value': True
}

float_data_object = {
    'type': 'float',
    'value': 2.7
}

string_data_object = {
    'type': 'string',
    'value': 'some text here'
}

string_data_object_array = {
    'type': 'string',
    'is_array': True,
    'members': [
        {
            'type': 'string',
            'value': 'text here'

        },
        {
            'type': 'string',
            'value': 'other text here'
        }
    ]
}

hash = {
    'value': '1234asfd',
    'function': 'md5', 
}

hash_2 = {
    'value': 'xyz123',
    'function': 'md5',
}

file_resource = {
    'upload_status': 'complete',
    'file_url': 'file:///absolute/path/to/my/file.txt',
    'md5': 'xqrtv',
}

file_resource_2 = {
    'upload_status': 'incomplete',
    'file_url': 'file:///absolute/path/to/my/file2.txt',
    'md5': 'jklmno'
}

file_data_object = {
    'type': 'file',
    'note': 'Here is where I got this',
    'source_url': 'file:///data/data/data/data.dat',
    'filename': 'file1.txt',
    'md5': 'xqrtv',
    'file_resource': file_resource,
    'source_type': 'imported'
}

file_data_object_without_resource = {
    'type': 'file',
    'note': 'Here is where I got this',
    'source_url': 'file:///data/data/data/data.dat',
    'filename': 'file1.txt',
    'md5': 'xqrtv',
    'source_type': 'imported'
}

file_data_object_2 = {
    'type': 'file',
    'note': 'More of the same',
    'source_url': 'file:///data/data2.dat',
    'filename': 'file2.txt',
    'file_resource': file_resource_2,
    'md5': 'jklmno',
    'source_type': 'imported'
}

file_data_object_array = {
    'type': 'file',
    'is_array': True,
    'members': [
        {
            'type': 'file',
            'note': 'Here is where I got this',
            'source_url': 'file:///data/data/data/data.dat',
            'filename': 'file.txt',
            'md5': 'xqrtv',
            'file_resource': file_resource,
            'source_type': 'imported'
        },
        {
            'type': 'file',
            'note': 'Here is where I got this',
            'source_url': 'file:///data/data/data/data1.dat',
            'filename': 'file1.txt',
            'md5': 'xqrtv',
            'file_resource': file_resource,
            'source_type': 'imported'
        },
    ]
}
