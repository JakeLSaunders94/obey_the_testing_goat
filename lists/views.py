from django.shortcuts import render, redirect
from .models import Item, List


def home_page(request):
    return render(request, 'home_page.html')


def view_list(request, list_id):
    list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list})


def new_list(request):
    if request.method == "POST":
        list = List.objects.create()
        new_todo = Item(text=request.POST['item_text'],
                        List=list)
        new_todo.save()
        return redirect('view_list', list_id=list.id)


def add_item(request, list_id):
    if request.method == "POST":
        text = request.POST.get('item_text', None)
        if text:
            list = List.objects.get(id=list_id)
            Item.objects.create(List=list,
                                text=text)
            return redirect('view_list', list_id=list_id)
