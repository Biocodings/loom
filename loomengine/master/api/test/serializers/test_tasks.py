from django.test import TestCase
from rest_framework import serializers

from api.serializers.tasks import *
from api.models.tasks import *
from api.models.data_objects import BooleanDataObject, StringDataObject, \
    FileResource, FileDataObject
from . import fixtures

def get_task():
    task = Task.objects.create(
        interpreter='/bin/bash',
        command='echo {{input1}}',
        rendered_command='echo True'
    )
    input_data_object = BooleanDataObject.objects.create(
        type='boolean',
        value=True
    )
    input = TaskInput.objects.create(task=task,
                                     data_object=input_data_object,
                                     channel='input1',
                                     type='boolean')
    output_data_object = StringDataObject.objects.create(
        type='string',
        value='answer'
    )
    task_output = TaskOutput.objects.create(
        task=task,
        channel='output1',
        type='string',
        data_object=output_data_object
    )
    task_output_source = TaskOutputSource.objects.create(
        task_output=task_output,
        stream='stdout'
    )
    task_resources = TaskResourceSet.objects.create(
        task=task,
        memory='1',
        disk_size='1',
        cores='1'
    )
    task_environment = TaskEnvironment.objects.create(
        task=task,
        docker_image='ubuntu'
    )
    task_attempt = TaskAttempt.objects.create(task=task)
    task_attempt_output = TaskAttemptOutput.objects.create(
        task_attempt=task_attempt,
        task_output=task_output,
        data_object=output_data_object
    )
    task_attempt_error = TaskAttemptError.objects.create(
        task_attempt=task_attempt,
        message='oops',
        detail='something went wrong')
    log_file_resource = FileResource.objects.create(
        **fixtures.data_objects.file_resource)
    log_file_data_object = FileDataObject.objects.create(
        type='file',
        filename='stderr.log',
        file_resource = log_file_resource,
        md5 = fixtures.data_objects.file_resource['md5'],
        source_type='log',
        )
    log_file = TaskAttemptLogFile.objects.create(
        task_attempt=task_attempt,
        log_name='stderr',
        file=log_file_data_object
    )

    return task

class TestTaskSerializer(TestCase):

    def testRender(self):
        task = get_task()
        s = TaskSerializer(task)
        task_data = s.data
        self.assertEqual(task_data['command'],
                         task.command)


class TestTaskSerializerIdOnly(TestCase):

    def testRender(self):
        task = get_task()
        s = TaskIdSerializer(task)
        task_data = s.data
        self.assertEqual(task_data['id'],
                         task.id.hex)

    
    