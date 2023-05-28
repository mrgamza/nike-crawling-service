import json

from django.http import HttpResponse
from rest_framework import status
from datetime import datetime
from pytz import timezone

from .controller import CrawlingController


def hello(request):
    return HttpResponse("Hi")


def job(request):
    recipients = request.GET.get('recipients', None)

    if recipients is None:
        return HttpResponse(json.dumps({"status": "required field not found"}),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_400_BAD_REQUEST)

    date = request.GET.get('date', None)
    time = request.GET.get('time', None)

    if date is None:
        now = datetime.now(timezone('Asia/Seoul'))
        year = now.year
        month = now.month
        day = now.day
    else:
        date_split = list(map(int, date.split("-")))
        year = date_split[0]
        month = date_split[1]
        day = date_split[2]

    return HttpResponse(CrawlingController.get_product(year, month, day, time, recipients),
                        content_type='application/json; charset=utf-8',
                        status=status.HTTP_200_OK)
