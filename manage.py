#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import requests

from apscheduler.schedulers.background import BackgroundScheduler


def job():
    requests.get("http://127.0.0.1:8000/job")

    
def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=60, id='job')
    scheduler.start()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nike_crawling_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
