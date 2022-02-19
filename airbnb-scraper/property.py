import re
import time
from inspect import cleandoc

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Property:
    def __init__(self, url=None, file=None):
        if url is not None:
            html = self.get_property_listing(url)
            self.data = self.parse_html(html)
        else:
            with open(file, "r", encoding='utf-8') as f:
                text = f.read()
            self.data = self.parse_html(text)

        self.property_name = self.get_property_name()
        self.property_details = self.get_property_details()

    def parse_html(self, html):
        return BeautifulSoup(html, "html5lib")

    def get_property_listing(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(service=Service(
            ChromeDriverManager(log_level=0).install()), options=chrome_options)
        browser.get(url)
        time.sleep(2)

        html = browser.page_source
        browser.quit()
        return html

    def get_property_name(self):
        name = self.data.find(
            attrs={"data-section-id": "TITLE_DEFAULT"}).find("h1")
        return name.get_text() if name is not None else "Property name not found"

    def get_property_details(self):
        overview = self.data.find(
            attrs={"data-section-id": "OVERVIEW_DEFAULT"}).find("ol")

        bedrooms = self.extract_property_details(overview, "bedroom", 1)
        bathrooms = self.extract_property_details(overview, "bathroom", 2)

        return {"bedrooms": bedrooms, "bathrooms": bathrooms}

    def extract_property_details(self, overview, detail_name, detail_index):
        property_detail = overview.find(
            "span", text=re.compile(detail_name))
        if property_detail is None:
            try:
                spans = overview.find_all("li")[
                    detail_index].find_all("span")
                property_detail_by_index = spans[1] if len(
                    spans) == 2 else spans[0]
            except IndexError as err:
                print(f"Cannot find property detail: {err}")
                property_detail_by_index = None
            property_detail = property_detail_by_index

        return property_detail.get_text() if property_detail is not None else f"unable to scrape {detail_name}s"

    def __str__(self):
        details = cleandoc(f"""Name: {self.property_name}
        Bedrooms: {self.property_details.get("bedrooms")}
        Bathrooms: {self.property_details.get("bathrooms")}
        {'-' * 30}
        """)
        return details

    def write_to_file(self, file_name, contents):
        f = open(file_name, "w")
        f.write(contents)
        f.close()
