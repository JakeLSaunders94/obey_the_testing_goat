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
        self.assertIn('A new list item', response.content.decode(), "The to-do list item could not be found in the response..")

    def test_response_shows_all_todo_items_for_user(self):
        test_todos = [
            'a test todo item',
            'something else',
            'more stuff'
        ]
        for items in test_todos:
            newitem = Item(text=items)
            newitem.save()

        all_user_todo_items = Item.objects.all()
        response = self.client.get("/")
        for todos in all_user_todo_items:
            self.assertIn(todos.text, response.content.decode(), f"The saved to-do list item {todos.text} could not be found in the response..")