from django.shortcuts import render, redirect
from .models import Item, List


def home_page(request):
    return render(request, 'home_page.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'todos': items})

def new_list(request):
    if request.method == "POST":
        list = List.objects.create()
        new_todo = Item(text=request.POST['item_text'],
                        List=list)
        new_todo.save()
        return redirect('/lists/the-only-list-in-the-world')
