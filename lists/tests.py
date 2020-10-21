from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse, HttpRequest
from .views import home_page

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home_page.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={'item_text': "A new list item"})
        self.assertIn('A new list item', response.content.decode(), "The to-do list item could not be found in the response..")