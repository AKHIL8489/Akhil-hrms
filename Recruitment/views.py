from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
import json
import datetime

@csrf_exempt
def jobPosting(request):
    data = json.loads(request.body)
    role = data['role']
    responsibilities = data['responsibilities']
    qualifications = data['qualifications']
    experience = data['experience']
    date = datetime.datetime.now()

    saveToDb = JobPost(designation=role, responsibilities=responsibilities, qualifications=qualifications, experience=experience,jobPostingDate = date)
    saveToDb.save()

    return JsonResponse({
        "status": "success",
        "message": "data received",
    })


@csrf_exempt
def viewAllPostedJobs(request):
    try:
        request.method = 'GET'

        job_posts = JobPost.objects.all()
        serialized_jobs = serializers.serialize('json', job_posts)
        allJobs = json.loads(serialized_jobs)

        return JsonResponse({
            "status":"success",
            "data": allJobs
        })

    except Exception as e:
        return JsonResponse({
            "status":"failed", 
            "message":str(e)
        })



