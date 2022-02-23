import re
import time
from inspect import cleandoc

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pathlib
import validators


class Property:
    def __init__(self, html=None, property_name=None, property_type=None, property_details=None):
        self.html = html
        self.property_name = property_name
        self.property_type = property_type
        self.property_details = property_details

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, value):
        if validators.url(value):
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

        self._html = BeautifulSoup(text, "html5lib") or None

    @property
    def property_name(self):
        return self._property_name

    @property_name.setter
    def property_name(self, property_name):
        if property_name:
            self._property_name = property_name
        elif self.html:
            try:
                found_name = self.html.find(
                    attrs={"data-section-id": "TITLE_DEFAULT"}).find("h1")
                self._property_name = found_name.get_text().strip()
            except AttributeError:
                self._property_name = "Property name not found"
        else:
            self._property_name = "Property name not found"

    @property
    def property_type(self):
        return self._property_type

    @property_type.setter
    def property_type(self, property_type):
        if property_type:
            self._property_type = property_type
        elif self.html:
            try:
                found_property_type = self.html.find(
                    attrs={"data-section-id": "OVERVIEW_DEFAULT"}).find("h2")
                self._property_type = found_property_type.get_text().split("hosted")[
                    0].strip()
            except AttributeError:
                self._property_type = "unable to find property type"
        else:
            self._property_type = "unable to find property type"

    @property
    def property_details(self):
        return self._property_details

    @property_details.setter
    def property_details(self, details):
        if details:
            self._property_details = {
                "bedrooms": details.bedrooms,
                "bathrooms": details.bathrooms
            }
        elif self.html:
            try:
                overview_list = self.html.find(
                    attrs={"data-section-id": "OVERVIEW_DEFAULT"}).find("ol")
                bedrooms = self.extract_property_details(
                    overview_list, "bedroom", 1)
                bathrooms = self.extract_property_details(
                    overview_list, "bathroom", 2)
                self._property_details = {
                    "bedrooms": bedrooms, "bathrooms": bathrooms}
            except AttributeError:
                self._property_details = {
                    "bedrooms": "Unable to find property detail", "bathrooms": "Unable to find property detail"}
        else:
            self._property_details = {
                "bedrooms": "Unable to find property detail", "bathrooms": "Unable to find property detail"}

    def extract_property_details(self, overview, detail_name, detail_index):
        try:
            property_detail = overview.find(
                "span", text=re.compile(detail_name))

            if property_detail:
                return property_detail.get_text().strip()
            else:
                spans = overview.find_all("li")[
                    detail_index].find_all("span")
                property_detail = spans[1] if len(
                    spans) == 2 else spans[0]
                if len(property_detail):
                    return property_detail.get_text().strip()
                else:
                    raise ValueError

        except (AttributeError, IndexError, ValueError):
            return "Unable to find property detail"

    def __str__(self):
        details = cleandoc(f"""Name: {self.property_name}
        Type: {self.property_type}
        Bedrooms: {self.property_details.get("bedrooms")}
        Bathrooms: {self.property_details.get("bathrooms")}
        {'-' * 30}
        """)
        return details
