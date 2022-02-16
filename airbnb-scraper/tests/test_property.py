import unittest
from property import Property


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.property = Property()

    def test_get_property_name(self):
        self.assertEqual(self.property.get_property_name(),
                         "123", "incorrect property name")
