from django.shortcuts import render
from .models import Item


def home_page(request):
    if request.method == "POST":
        new_todo = Item(text=request.POST.get('item_text'))
        new_todo.save()

    all_items = Item.objects.all()
    return render(request, 'home_page.html', {'todos': all_items})


