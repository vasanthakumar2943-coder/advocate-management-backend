from django.urls import path
from .views import create_appointment, advocate_requests, approve_appointment
from django.http import HttpResponse

def test_api(request):
    return HttpResponse("USERS URL WORKING")


urlpatterns = [
    path("appointments/", create_appointment),
    path("appointments/requests/", advocate_requests),
    path("appointments/approve/<int:pk>/", approve_appointment),
    path("test/", test_api),
     path("appointments/", create_appointment),

]
