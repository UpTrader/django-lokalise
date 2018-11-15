import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import handle_content


@csrf_exempt
def hook(request):
    file_name = request.POST.get('file')

    if file_name:
        r = requests.get('https://lokalise.co/{0}'.format(file_name))
        if r.status_code == 200:
            handle_content(r.content)

    return HttpResponse('')
