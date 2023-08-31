from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def startTimer(request):
    print("timer started")
    
@csrf_exempt
def stopTimer(request):
    print("timer stopped")
