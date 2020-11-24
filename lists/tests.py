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
    def test_displays_all_items_for_that_list(self):
        list = List.objects.create()
        Item.objects.create(text="testy 1",
                            List=list)
        Item.objects.create(text="testy 2",
                            List=list)

        list2 = List.objects.create()
        Item.objects.create(text="testy 1 not your list",
                            List=list2)
        Item.objects.create(text="testy 2 not your list",
                            List=list2)

        response = self.client.get(f'/lists/current/{list.id}')
        self.assertContains(response, 'testy 1')
        self.assertContains(response, 'testy 2')
        self.assertNotContains(response, 'testy 1 not your list')
        self.assertNotContains(response, 'testy 2 not your list')

    def test_uses_correct_template(self):
        list = List.objects.create()
        response = self.client.get(f'/lists/current/{list.id}')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        list = List.objects.create()
        list2 = List.objects.create()

        response = self.client.get(f'/lists/current/{list2.id}')
        self.assertEqual(response.context['list'], list2)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post("/lists/new", data={'item_text': "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.all().first()
        self.assertEqual(saved_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={'item_text': "A new list item"})
        self.assertRedirects(response, '/lists/current/1', 302)


class NewItemTest(TestCase):
    def test_can_add_new_items_to_an_existing_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()

        self.client.post('/lists/current/1/add_item', {'item_text': "The item for my list"})
        self.client.post('/lists/current/2/add_item', {'item_text': "Something for my second list"})

        self.assertEqual(Item.objects.filter(List=list1).count(), 1)
        self.assertEqual(Item.objects.filter(List=list1)[0].text, "The item for my list")
        self.assertEqual(Item.objects.filter(List=list2).count(), 1)
        self.assertEqual(Item.objects.filter(List=list2)[0].text, "Something for my second list")
