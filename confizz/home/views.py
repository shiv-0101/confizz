from django.shortcuts import render

def index(request):
    print("Homepage view is called")
    return render(request, 'home/index.html')
