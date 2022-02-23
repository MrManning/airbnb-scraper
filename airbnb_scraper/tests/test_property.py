import os
import unittest
from property.property import Property


class TestProperty(unittest.TestCase):
    directory = os.path.dirname(__file__)

    def setUp(self):
        self.property = Property("https://www.airbnb.co.uk/rooms/45885953")

        test_property_1 = os.path.join(
            TestProperty.directory, "property_with_different_bathroom.html")
        self.property_with_different_bathroom = Property(test_property_1)

        test_property_2 = os.path.join(
            TestProperty.directory, "property_with_no_overview.html")
        self.property_with_no_overview = Property(test_property_2)

    def test_get_property_name_with_valid_html(self):
        # print("inside the test function")
        # print(self.property)
        self.assertEqual(self.property.property_name,
                         "Luxury Kabin Surrounded by Nature + Outdoor Bath!", "incorrect property name")

    def test_get_property_name_with_missing_html(self):
        self.assertEqual(self.property_with_different_bathroom.property_name,
                         "Property name not found")

    def test_get_property_details_with_valid_html(self):
        self.assertDictEqual(self.property.property_details, {
            "bedrooms": "1 bedroom",
            "bathrooms": "1 bathroom"
        })

    def test_get_property_details_with_non_standard_bathroom(self):
        self.assertDictEqual(self.property_with_different_bathroom.property_details, {
            "bedrooms": "2 bedrooms",
            "bathrooms": "Toilet with sink"
        })

    def test_get_property_details_with_no_bathroom(self):
        self.assertEqual(self.property_with_no_overview.property_details, {
            "bedrooms": "Unable to find property detail",
            "bathrooms": "Unable to find property detail"
        })

    def test_print_property(self):
        self.assertEqual(
            str(self.property), f"Name: Luxury Kabin Surrounded by Nature + Outdoor Bath!\nType: Tiny house\nBedrooms: 1 bedroom\nBathrooms: 1 bathroom\n{'-' * 30}")


if __name__ == "__main__":
    unittest.main()
