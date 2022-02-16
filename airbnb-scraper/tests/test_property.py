import unittest
from property import Property


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.property = Property("https://www.airbnb.co.uk/rooms/45885953")

    def test_get_property_name_with_valid_html(self):
        self.assertEqual(self.property.get_property_name(),
                         "123", "incorrect property name")

    def test_get_property_name_with_invalid_html(self):
        self.assertEqual(self.property.get_property_name(),
                         "", "incorrect property name")

    def test_get_property_details_with_valid_html(self):
        self.assertEqual(self.property.get_property_details(),
                         ["bedrooms", "bathrooms"])

    def test_get_property_details_with_invalid_html(self):
        self.assertEqual(self.property.get_property_details(),
                         [])

    def test_get_property_amenities_with_valid_html(self):
        self.assertEqual(self.property.get_property_amenities(), "")

    def test_get_property_amenities_with_invalid_html(self):
        self.assertEqual(self.property.get_property_amenities(), "")

    def test_print_property(self):
        self.assertEqual()
