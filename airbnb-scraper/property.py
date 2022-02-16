from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class Property:
    def __init__(self, url):
        self.data = self.get_property_listing(url)
        self.property_name = self.get_property_name()

    def get_property_listing(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(service=Service(
            ChromeDriverManager(log_level=0).install()), options=chrome_options)
        browser.get(url)
        time.sleep(2)

        raw_html = BeautifulSoup(browser.page_source, "html.parser")
        browser.quit()
        return raw_html

    def get_property_name(self):
        name = self.data.find(
            attrs={"data-section-id": "TITLE_DEFAULT"}).find("h1")
        return name.get_text() if name is not None else ""

    def print_property(self):
        print(f"Name: {self.property_name}\n{'-' * 20}")

    def write_to_file(self, file_name, contents):
        f = open(file_name, "w")
        f.write(contents)
        f.close()
