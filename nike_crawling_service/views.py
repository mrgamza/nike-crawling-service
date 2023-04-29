from django.http import HttpResponse
from .controller import crawling_controller


def hello(request):
    return HttpResponse("Hi")


def job(request):
    parsing_option = request.GET.get('parsing_option', 'date,time')
    result = crawling_controller.get_product(parsing_option, False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')
