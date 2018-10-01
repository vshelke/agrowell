from django.shortcuts import render
from django.http import HttpResponse
import ag_dashboard.modules.db as db
import datetime

# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/dashboard.html')
    return render(request, 'general/index.html')

def api(request, plant, date, degree):
    if request.user.is_authenticated:
        date = datetime.datetime.strptime(date, "%d-%m-%Y")
        return HttpResponse(db.getData(plant, date, int(degree)), status=200, content_type='application/json')
    return render(request, 'general/index.html')
    # return date