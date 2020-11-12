from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse, HttpRequest
from .views import home_page
from .models import Item

class ModelTests(TestCase):
    def test_creating_and_retrieving_todo_items(self):
        item = Item(text="The first to-do item")
        item.save()

        item = Item(text="The second to-do item")
        item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)



class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home_page.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={'item_text': "A new list item"})
        saved_item = Item.objects.all().first()
        self.assertEqual(saved_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/", data={'item_text': "A new list item"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world')

    def test_doesnt_save_items_for_no_reason(self):
        self.client.get("/")
        self.assertEqual(Item.objects.all().count(), 0)


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text="testy 1")
        Item.objects.create(text="testy 2")

        response = self.client.get('/lists/the-only-list-in-the-world')
        self.assertContains(response, 'testy 1')
        self.assertContains(response, 'testy 2')

    def test_uses_correct_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world')
        self.assertTemplateUsed(response, 'list.html')
