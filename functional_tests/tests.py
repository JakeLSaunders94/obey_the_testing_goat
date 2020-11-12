from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import unittest
MAX_WAIT = 5
class GeneralSeleniumFunctions:
    def wait_for_object_by_id(self, driver, object_id, wait_time=MAX_WAIT):
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, object_id))
            )
            return True
        except:
            return False


class NewVisitorTest(LiveServerTestCase, GeneralSeleniumFunctions):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_todo_item(self, item_text, wait_time):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(item_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > wait_time:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)


        self.wait_for_todo_item('1: Buy peacock feathers', 5)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_todo_item("2: Use peacock feathers to make a fly", 5)

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail("Finish your test!")

    def test_multiple_users_can_start_lists_st_different_URLS(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)

        box = self.browser.find_element_by_id('id_new_item')
        box.send_keys('Buy peacock feathers')
        box.send_keys(Keys.ENTER)
        self.wait_for_todo_item('1: Buy peacock feathers', 5)

        # Edith notices her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Our second new user, Dave, comes to the site (on a new browser instance)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Dave goes ont his new list, he doesn't care about fly fishing. Edith's list isn't shown.
        self.browser.get(self.live_server_url)
        page_tect = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_tect)
        self.assertNotIn('Make a fly', page_tect)

        # Dave starts his own list, dave is into 2nd world war reinactment
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Buy Sherman Tank")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_todo_item("2: Buy Sherman Tank", 5)

        # Dave also gets his own URL
        dave_list_url = self.browser.current_url
        self.assertRegex(dave_list_url, '/lists/.+')
        self.assertNotEqual(dave_list_url, edith_list_url)

        # Still no sign of edith's list (what would a guy who owns a tank do with fly fishing equipment?)
        self.browser.get(self.live_server_url)
        page_tect = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_tect)
        self.assertNotIn('Make a fly', page_tect)
