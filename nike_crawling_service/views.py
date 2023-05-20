import json

from django.http import HttpResponse
from rest_framework import status
from datetime import datetime
from pytz import timezone

from .controller import CrawlingController


def hello(request):
    return HttpResponse("Hi")


def job(request):
    now = datetime.now(timezone('Asia/Seoul'))

    year = request.GET.get('year', now.year)
    month = request.GET.get('month', now.month)
    day = request.GET.get('day', now.day)
    recipients = request.GET.get('recipients', None)

    if recipients is None:
        return HttpResponse(json.dumps({"status": "required field not found"}),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(CrawlingController.get_product(year, month, day, recipients),
                        content_type='application/json; charset=utf-8')
