from django.shortcuts import render

def home_page(request):
    if request.method == "POST":


    return render(request, 'home_page.html')


