from django.shortcuts import render, redirect
from .models import Item


def home_page(request):
    return render(request, 'home_page.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'todos': items})

def new_list(request):
    if request.method == "POST":
        new_todo = Item(text=request.POST['item_text'])
        new_todo.save()
        return redirect('/lists/the-only-list-in-the-world')
