import re
import time
from inspect import cleandoc

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pathlib


class Property:
    def __init__(self, html=None):
        self.html = html
        self.property_name = self.get_property_name()
        self.property_details = self.get_property_details()

    def get_html(self):
        return self._html

    def set_html(self, value):
        protocols = ["https://", "http://"]
        domains = [".co.uk", ".com"]

        if value.startswith(tuple(protocols)) or value.endswith(tuple(domains)) and "\n" not in value:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            browser = webdriver.Chrome(service=Service(
                ChromeDriverManager(log_level=0).install()), options=chrome_options)
            browser.get(value)
            time.sleep(2)

            text = browser.page_source
            browser.quit()
        elif pathlib.Path(value).exists():
            with open(value, "r") as f:
                text = f.read()
        else:
            text = value

        self._html = BeautifulSoup(text, "html5lib")

    def get_property_name(self):
        name = self.html.find(
            attrs={"data-section-id": "TITLE_DEFAULT"}).find("h1")
        return name.get_text() if name is not None else "Property name not found"

    def get_property_details(self):
        overview = self.html.find(
            attrs={"data-section-id": "OVERVIEW_DEFAULT"})
        overview_list = overview.find("ol")

        bedrooms = self.extract_property_details(overview_list, "bedroom", 1)
        bathrooms = self.extract_property_details(overview_list, "bathroom", 2)
        property_type = self.get_property_type(overview)

        return {"type": property_type, "bedrooms": bedrooms, "bathrooms": bathrooms}

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

        return property_detail.get_text() if len(property_detail) else f"unable to find {detail_name}s"

    def get_property_type(self, overview):
        header = overview.find("h2")
        try:
            if len(header):
                return header.get_text().split("hosted")[0].strip()
        except TypeError:
            return "unable to find property type"

    def __str__(self):
        details = cleandoc(f"""Name: {self.property_name}
        Type: {self.property_details.get("type")}
        Bedrooms: {self.property_details.get("bedrooms")}
        Bathrooms: {self.property_details.get("bathrooms")}
        {'-' * 30}
        """)
        return details

    html = property(get_html, set_html)
