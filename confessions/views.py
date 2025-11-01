import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import google.generativeai as genai

def hello_world(request):
    return render(request, "confessions/helloworld.html")
