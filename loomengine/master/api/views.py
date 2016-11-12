from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
import os
from rest_framework import viewsets

from api import get_setting
from api import models
from api import serializers
from loomengine.utils import version


logger = logging.getLogger(__name__)

class DataObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DataObjectSerializer
    queryset = models.DataObject.objects.all()

"""
class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TemplateSerializer
    queryset = models.Template.objects.all()

    def get_queryset(self):
        query_string = self.request.query_params.get('q', '')
        if query_string:
            queryset = models.FileDataObject.query(query_string)
        else:
            queryset = models.FileDataObject.objects.all()
        return queryset
"""

"""
class AbstractWorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AbstractWorkflowSerializer

    def get_queryset(self):
        query_string = self.request.query_params.get('q', '')
        if query_string:
            queryset = models.AbstractWorkflow.query(query_string)
        else:
            queryset = models.AbstractWorkflow.objects.all()
        return queryset

class ImportedWorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AbstractWorkflowSerializer

    def get_queryset(self):
        query_string = self.request.query_params.get('q', '')
        if query_string:
            queryset = models.AbstractWorkflow.query(query_string)
        else:
            queryset = models.AbstractWorkflow.objects.all()
        return queryset.filter(workflow_import__isnull=False).order_by('-datetime_created')
    
class FileLocationViewSet(viewsets.ModelViewSet):
    queryset = models.FileLocation.objects.all()
    serializer_class = serializers.FileLocationSerializer

class FileImportViewSet(viewsets.ModelViewSet):
    queryset = models.FileImport.objects.all()
    serializer_class = serializers.FileImportSerializer

class FileDataObjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FileDataObjectSerializer

    def get_queryset(self):
        query_string = self.request.query_params.get('q', '')
        if query_string:
            queryset = models.FileDataObject.query(query_string)
        else:
            queryset = models.FileDataObject.objects.all()
        return queryset

class FileProvenanceViewSet(viewsets.ModelViewSet):
    queryset = models.FileDataObject.objects.all()
    serializer_class = serializers.FileProvenanceSerializer

class ImportedFileDataObjectViewSet(viewsets.ModelViewSet):
    queryset = models.FileDataObject.objects.filter(source_type='imported').order_by('-datetime_created')
    serializer_class = serializers.FileDataObjectSerializer

class ResultFileDataObjectViewSet(viewsets.ModelViewSet):
    queryset = models.FileDataObject.objects.filter(source_type='result').order_by('-datetime_created')
    serializer_class = serializers.FileDataObjectSerializer

class LogFileDataObjectViewSet(viewsets.ModelViewSet):
    queryset = models.FileDataObject.objects.filter(source_type='log').order_by('-datetime_created')
    serializer_class = serializers.FileDataObjectSerializer

class RunRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RunRequestSerializer

    def get_queryset(self):
        query_string = self.request.query_params.get('q', '')
        if query_string:
            queryset = models.RunRequest.query(query_string)
        else:
            queryset = models.RunRequest.objects.all()
        return queryset.order_by('-datetime_created')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.tasks.Task.objects.all()
    serializer_class = serializers.TaskSerializer

class TaskAttemptErrorViewSet(viewsets.ModelViewSet):
    queryset = models.tasks.TaskAttemptError.objects.all()
    serializer_class = serializers.TaskAttemptErrorSerializer

class TaskAttemptOutputViewSet(viewsets.ModelViewSet):
    queryset = models.tasks.TaskAttemptOutput.objects.all()
    serializer_class = serializers.TaskAttemptOutputSerializer

class AbstractWorkflowRunViewSet(viewsets.ModelViewSet):
    queryset = models.AbstractWorkflowRun.objects.all()
    serializer_class = serializers.AbstractWorkflowRunSerializer

class TaskAttemptViewSet(viewsets.ModelViewSet):
    queryset = models.tasks.TaskAttempt.objects.all()
    serializer_class = serializers.TaskAttemptSerializer
"""

@require_http_methods(["GET"])
def status(request):
    return JsonResponse({"message": "server is up"}, status=200)

@require_http_methods(["GET"])
def worker_settings(request, id):
    try:
        task_attempt = models.TaskAttempt.objects.get(id=id)
        return JsonResponse({
            'WORKING_DIR': task_attempt.get_working_dir(),
            'STDOUT_LOG_FILE': task_attempt.get_stdout_log_file(),
            'STDERR_LOG_FILE': task_attempt.get_stderr_log_file(),
        }, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=404)
    except Exception as e:
        return JsonResponse({"message": e.message}, status=500)

@require_http_methods(["GET"])
def filemanager_settings(request):
    return JsonResponse({
        'PROJECT_ID': get_setting('PROJECT_ID'),
    })

@require_http_methods(["GET"])
def info(request):
    data = {
        'version': version.version()
    }
    return JsonResponse(data, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def create_task_attempt_log_file(request, id):
    data_json = request.body
    data = json.loads(data_json)
    try:
        task_attempt = models.TaskAttempt.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=404)
    s = serializers.TaskAttemptLogFileSerializer(
        data=data,
        context={
            'parent_field': 'task_attempt',
            'parent_instance': task_attempt
        })
    s.is_valid(raise_exception=True)
    model = s.save()
    return JsonResponse(s.data, status=201)

@csrf_exempt
@require_http_methods(["POST"])
def create_task_attempt_error(request, id):
    data_json = request.body
    data = json.loads(data_json)
    try:
        task_attempt = models.TaskAttempt.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Not Found"}, status=404)
    s = serializers.TaskAttemptErrorSerializer(
        data=data,
        context={
            'parent_field': 'task_attempt',
            'parent_instance': task_attempt
        })
    s.is_valid(raise_exception=True)
    model = s.save()
    return JsonResponse(s.data, status=201)

