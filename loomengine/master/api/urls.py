from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

import api.views

router = routers.DefaultRouter()

router.register('data-objects',
                api.views.DataObjectViewSet,
                base_name='data-object')
router.register('data-files',
                api.views.FileDataObjectViewSet,
                base_name='data-file')
router.register('data-strings',
                api.views.StringDataObjectViewSet,
                base_name='data-string')
router.register('data-booleans',
                api.views.BooleanDataObjectViewSet,
                base_name='data-boolean')
router.register('data-integers',
                api.views.IntegerDataObjectViewSet,
                base_name='data-integer')
router.register('data-floats',
                api.views.FloatDataObjectViewSet,
                base_name='data-float')
router.register('data-arrays',
                api.views.ArrayDataObjectViewSet,
                base_name='data-array')
router.register('data-trees',
                api.views.DataTreeViewSet,
                base_name='data-tree')
router.register('file-resources',
                api.views.FileResourceViewSet,
                base_name='file-resource')
router.register('tasks',
                api.views.TaskViewSet,
                base_name='task')
router.register('task-attempts',
                api.views.TaskAttemptViewSet,
                base_name='task-attempt')
router.register('task-attempt-outputs',
                api.views.TaskAttemptOutputViewSet,
                base_name='task-attempt-output')
router.register('task-attempt-log-files',
                api.views.TaskAttemptLogFileViewSet,
                base_name='task-attempt-log-file')
router.register('templates',
                api.views.TemplateViewSet,
                base_name='template')
router.register('runs',
                api.views.RunViewSet,
                base_name='run')
router.register('run-requests',
                api.views.RunRequestViewSet,
                base_name='run-request')

# file_provenance_detail = api.views.FileProvenanceViewSet.as_view({'get':'retrieve'})

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^status/$', api.views.status),
    url(r'^info/$', api.views.info),
    url(r'^filemanager-settings/$', api.views.filemanager_settings),
    url('^doc/$', get_swagger_view(title='Loom API')),
    #    url(r'^files/(?P<pk>[a-zA-Z0-9]+)/provenance/$', file_provenance_detail, name='file_provenance_detail'),
]
