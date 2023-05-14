from django.http import HttpResponse
from .controller import CrawlingController


def hello(request):
    return HttpResponse("Hi")


def job(request):
    parsing_option = request.GET.get('parsing_option', 'date,time')
    recipients = request.GET.get('recipients', '')
    result = CrawlingController.get_product(parsing_option, recipients)
    return HttpResponse(result, content_type='application/json; charset=utf-8')
