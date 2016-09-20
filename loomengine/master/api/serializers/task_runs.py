from rest_framework import serializers

from .base import CreateWithParentModelSerializer, SuperclassModelSerializer
from api.models.task_runs import TaskRun, TaskRunInput, TaskRunOutput,\
    TaskRunAttempt, TaskRunAttemptInput, TaskRunAttemptOutput, \
    TaskRunAttemptLogFile, WorkerProcess, WorkerProcessMonitor, WorkerHost
from api.serializers.data_objects import FileImportSerializer, DataObjectSerializer, FileDataObjectSerializer
from api.serializers.task_definitions import TaskDefinitionSerializer
from api.serializers.workflows import RequestedResourceSetSerializer


class TaskRunAttemptOutputSerializer(CreateWithParentModelSerializer):

    data_object = DataObjectSerializer(allow_null=True, required=False)
    type = serializers.CharField(read_only=True)
    channel = serializers.CharField(read_only=True)
    filename = serializers.CharField(read_only=True)

    class Meta:
        model = TaskRunAttemptOutput
        fields = ('id', 'data_object', 'filename', 'type', 'channel',)

    def update(self, instance, validated_data):
        data_object_data = self.initial_data.get('data_object', None)
        validated_data.pop('data_object', None)

        s = DataObjectSerializer(data=data_object_data)
        s.is_valid(raise_exception=True)
        validated_data['data_object'] = s.save()

        return super(self.__class__, self).update(
            instance,
            validated_data)


class TaskRunAttemptInputSerializer(CreateWithParentModelSerializer):

    data_object = DataObjectSerializer(allow_null=True, required=False)
    type = serializers.CharField(read_only=True)
    channel = serializers.CharField(read_only=True)

    class Meta:
        model = TaskRunAttemptInput
        fields = ('id', 'data_object', 'type', 'channel',)


class TaskRunAttemptLogFileSerializer(CreateWithParentModelSerializer):

    file_data_object = FileDataObjectSerializer(allow_null=True, required=False)

    class Meta:
        model = TaskRunAttemptLogFile
        fields = ('log_name', 'file_data_object',)


class WorkerHostSerializer(CreateWithParentModelSerializer):
    
    id = serializers.UUIDField(format='hex', required=False)

    class Meta:
        model = WorkerHost
        fields = ('id', 'status',)


class WorkerProcessSerializer(CreateWithParentModelSerializer):
    
    id = serializers.UUIDField(format='hex', required=False)

    class Meta:
        model = WorkerProcess
        fields = ('id', 'status', 'status_message', 'container_id')


class WorkerProcessMonitorSerializer(CreateWithParentModelSerializer):
    
    id = serializers.UUIDField(format='hex', required=False)
    
    class Meta:
        model = WorkerProcessMonitor
        fields = ('id', 'status', 'last_update')


class TaskRunAttemptSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(format='hex', required=False)
    name = serializers.CharField()
    log_files = TaskRunAttemptLogFileSerializer(many=True, allow_null=True, required=False)
    inputs = TaskRunAttemptInputSerializer(many=True, allow_null=True, required=False)
    outputs = TaskRunAttemptOutputSerializer(many=True, allow_null=True, required=False)
    task_definition = TaskDefinitionSerializer()
    worker_host = WorkerHostSerializer()
    worker_process = WorkerProcessSerializer()
    worker_process_monitor = WorkerProcessMonitorSerializer()

    class Meta:
        model = TaskRunAttempt
        fields = ('id', 'name', 'log_files', 'inputs', 'outputs', 'status', 'status_message', 'task_definition', 'worker_process', 'worker_process_monitor', 'worker_host')
        
    def update(self, instance, validated_data):
        status = validated_data.pop('status', None)
        if status is not None:
            instance.status = status
            instance.save()
        return instance

        
class TaskRunInputSerializer(CreateWithParentModelSerializer):

    data_object = DataObjectSerializer()
    type = serializers.CharField(read_only=True)
    channel = serializers.CharField(read_only=True)

    class Meta:
        model = TaskRunInput
        fields = ('data_object', 'type', 'channel',)


class TaskRunOutputSerializer(CreateWithParentModelSerializer):

    data_object = DataObjectSerializer()
    type = serializers.CharField(read_only=True)
    channel = serializers.CharField(read_only=True)
    filename = serializers.CharField(read_only=True)

    class Meta:
        model = TaskRunOutput
        fields = ('data_object', 'filename', 'type', 'channel',)


class TaskRunIdSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(format='hex', required=False)

    class Meta:
        model = TaskRun
        fields = ('id',)


class TaskRunSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(format='hex', required=False)
    name = serializers.CharField()
    task_definition = TaskDefinitionSerializer()
    resources = RequestedResourceSetSerializer()
    inputs = TaskRunInputSerializer(many=True, allow_null=True, required=False)
    outputs = TaskRunOutputSerializer(many=True, allow_null=True, required=False)
    task_run_attempts = TaskRunAttemptSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = TaskRun
        fields = ('id', 'name', 'task_definition', 'resources', 'inputs', 'outputs', 'task_run_attempts',)
