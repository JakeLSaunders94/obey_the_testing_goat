from django.shortcuts import render, redirect
from .models import Item


def home_page(request):
    if request.method == "POST":
        new_todo = Item(text=request.POST['item_text'])
        new_todo.save()
        return redirect('home_page')

    all_items = Item.objects.all()
    return render(request, 'home_page.html', {'todos': all_items})


