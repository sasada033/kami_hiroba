from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver

class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path='C:/Users/sasada/Desktop/python/chromedriver_win32/chromedriver.exe')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('http://localhost:8000' + str(reverse_lazy('account_login')))

        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('shk@ghh.com')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('sasada419')
        self.selenium.find_element_by_class_name('btn').click()

        self.assertEquals('記事一覧 | カミヒロバ', self.selenium.title)