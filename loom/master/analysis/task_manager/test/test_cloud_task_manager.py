#!/usr/bin/env python
import sys
import unittest

from django.conf import settings

import libcloud.compute.base

from loom.master.analysis.task_manager import cloud 
from loom.common.helper import on_gcloud_vm


@unittest.skipIf(not on_gcloud_vm(), 'not running on Google Compute Engine VM')
class TestCloudTaskManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not settings.configured:
            settings.configure()

    @classmethod
    def tearDownClass(cls):
        pass
        
    def setUp(self):
        settings.BASE_DIR = ''
        settings.MASTER_TYPE = 'GOOGLE_CLOUD'
        settings.PROJECT_ID = 'gbsc-gcp-project-scgs-dev'
        settings.ANSIBLE_PEM_FILE = '~/key.pem'
        settings.GCE_KEY_FILE = '~/.ssh/google_compute_engine'
        settings.WORKER_VM_IMAGE = 'container-vm'
        settings.WORKER_LOCATION = 'us-central1-a'
        settings.WORKER_DISK_TYPE = 'pd-ssd'
        settings.WORKER_DISK_SIZE = '100'
        settings.WORKER_DISK_MOUNT_POINT = '/mnt/loom_working_dir'

    def tearDown(self):
        pass

    def test_invalid_cloud_type(self):
        settings.MASTER_TYPE = 'INVALID_CLOUD_TYPE'

        with self.assertRaises(cloud.CloudTaskManagerError):
            cloud.CloudTaskManager._run('task')

    def test_get_gcloud_pricelist(self):
        pricelist = cloud.CloudTaskManager._get_gcloud_pricelist()
        self.assertIsInstance(pricelist, dict)

    def test_get_cheapest_instance_type(self):
        """ May need to be updated if prices change.""" 
        cheapest_type = cloud.CloudTaskManager._get_cheapest_instance_type(cores=1, memory=4)
        self.assertEquals(cheapest_type, 'n1-standard-2')
        
    def test_huge_instance_request(self):
        """ May need to be updated if Google starts offering supercomputer instances.""" 
        with self.assertRaises(cloud.CloudTaskManagerError):
            cloud.CloudTaskManager._get_cheapest_instance_type(cores=sys.maxint, memory=sys.float_info.max)

    def test_setup_ansible_gce(self):
        cloud.CloudTaskManager._setup_ansible_gce()
        import secrets
        self.assertIsInstance(secrets.GCE_PARAMS, tuple)
        self.assertIsInstance(secrets.GCE_KEYWORD_PARAMS, dict)

    def test_create_task_run(self):
        import loom.common.fixtures.general.task_runs
        #from loom.master.analysis.models.task_runs import TaskRun
        #TODO: use a real task run

    @unittest.skip('Skipping VM bootup test')
    def test_run(self):
        from collections import namedtuple
        Resources = namedtuple('Resources', 'cores memory')
        resources = Resources(cores=1, memory=1)
        TaskRun = namedtuple('TaskRun', 'id tasks')
        task_run = TaskRun(id = 'unittest-cloud-task-manager-run',
                           tasks = [resources])
        cloud.CloudTaskManager._run(task_run)

if __name__ == '__main__':
    unittest.main()