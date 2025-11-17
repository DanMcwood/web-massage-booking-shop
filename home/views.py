from django.shortcuts import render

def contacts(request):
    return render(request, 'home/contacts.html')

def home(request):
    return render(request, 'home/home.html')
