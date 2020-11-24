from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse, HttpRequest
from .views import home_page
from .models import Item, List

class ModelTests(TestCase):
    def test_creating_and_retrieving_todo_items(self):
        list = List()
        list.save()

        item = Item(text="The first to-do item")
        item.List = list
        item.save()

        item = Item(text="The second to-do item")
        item.List = list
        item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        # Check that the two list items have the correct text and the correct list
        self.assertEqual(Item.objects.filter(List=list,
                                             text="The first to-do item").count(), 1)
        self.assertEqual(Item.objects.filter(List=list,
                                             text="The second to-do item").count(), 1)



class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home_page.html')

class ListViewTest(TestCase):
    def test_displays_all_items(self):
        list = List.objects.create()
        Item.objects.create(text="testy 1",
                            List=list)
        Item.objects.create(text="testy 2",
                            List=list)

        response = self.client.get('/lists/the-only-list-in-the-world')
        self.assertContains(response, 'testy 1')
        self.assertContains(response, 'testy 2')

    def test_uses_correct_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post("/lists/new", data={'item_text': "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.all().first()
        self.assertEqual(saved_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={'item_text': "A new list item"})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world', 302)
