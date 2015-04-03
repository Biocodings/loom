from django.db import models


"""

class PipelineRunRequest(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    pipeline = models.ForeignKey(Pipeline)

    @classmethod
    def create_from_json(cls, raw_data_json):
        results_request=cls()
        results_request.pipeline = Pipeline.find_or_create(raw_data_json)
        results_request._get_results()
        results_request.save()

    def _get_results(self):
        if self.pipeline.has_results():
            self._return_results(pipeline.results)
        else:
            self._request_pipeline_run()
            self._send_receipt()

    def _request_pipeline_run(self):
        self.run_request = PipelineRunRequest.find_or_create(pipeline=self.pipeline)

    def _send_receipt(self):
        #TODO
        return
    
# A request comes in. JSON data is saved raw in PipelineRunRequest.
# Check for inputs. Error if we don't have them.
# Check for pipeline. Create it if it doesn't exist.
# Check for results. Return them if they exist.
# Create a PipelineRunRequest and link PipelineResultsRequest to it.

class Session(models.Model):
    comments = models.CharField()
#    session_resources = models.OneToOneField(SessionResources)

class LocalFile(models.Model):
    comments = models.CharField()
    name = models.CharField()
    path = models.CharField()

class Application(models.Model):
    comments = models.CharField()
    name = models.CharField()
    docker_image = models.CharField()

class LocalFile(models.Model):
    comments = models.CharField()
    name = models.CharField()
    path = models.CharField()

class ExternalFileLocation(models.Model):
    comments = models.CharField()
    path = models.CharField()

class Import(models.Model):
    comments = models.CharField()
    import_file = models.OneToOneField(LocalFile, related_name='import')
    source = models.OneToOneField(ExternalFileLocation)

class Export(models.Model):
    comments = models.CharField()
    export_file = models.OneToOneField(LocalFile, related_name='export')
    destination = models.OneToOneField(ExternalFileLocation)

class SessionResources(models.Model):
    comments = models.CharField()
    disk_space = models.CharField()
    memory = models.CharField()
    cores = models.PositiveIntegerField()

class TaskResources(models.Model):
    comments = models.CharField()
    memory = models.CharField()
    cores = models.PositiveIntegerField()



class _InputData(object):

    def _process_json(self, data_json):
        dirty_nested_data = json.loads(data_json)
        dirty_data = self._flatten(dirty_nested_data)
        data = self._clean(dirty_data)
        return data

    def _flatten(self, data):
        #TODO
        return data

    def _clean(self, data):
        #TODO
        return data


class Step(models.Model):
    comments = models.CharField()
    command = models.CharField()
    application = models.ForeignKey(Application)
    input_files = models.ManyToManyField(LocalFile, related_name = 'input_for_steps')
    output_files = models.ManyToManyField(LocalFile, related_name = 'output_from_step')
    resources = models.OneToOneField(TaskResources)
    session = models.ForeignKey(Session)


"""