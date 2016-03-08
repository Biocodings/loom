from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from analysis.models import WorkflowRun, TaskRun
from loomdaemon import loom_daemon_logger


class Command(BaseCommand):
    help = 'Checks and updates work in progress'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--logfile',
            dest='logfile',
            default=None,
            help='Log file path')

    @transaction.atomic
    def handle(self, *args, **options):
        logfile = options.get('logfile')
        logger = loom_daemon_logger.get_logger(logfile)
        try:
            WorkflowRun.update_status_for_all()
            TaskRun.run_all()
        except Exception as e:
            logger.exception(e)
            raise
