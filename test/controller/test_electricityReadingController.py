import unittest

from .setup_test_app import app

class TestElectricityReadingController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_successfully_add_the_reading_against_new_smart_meter_id(self):
        readingJson = {
            "smartMeterId": "meter-11",
            "electricityReadings": [
                {"time": 1505825656, "reading": 0.6}
            ]
        }

        response = self.client.post('/readings/store', json=readingJson)
        self.assertEqual(200, response.status_code)

    def test_successfully_add_the_reading_against_existing_smart_meter_id(self):
        readingJson1 = {
            "smartMeterId": "meter-100",
            "electricityReadings": [
                { "time": 1505825838, "reading": 0.6 },
                { "time": 1505825848, "reading": 0.65 },
            ]
        }

        readingJson2 = {
            "smartMeterId": "meter-100",
            "electricityReadings": [
                { "time": 1605825849, "reading": 0.7 }
            ]
        }

        self.client.post('/readings/store', json=readingJson1)
        self.client.post('/readings/store', json=readingJson2)
        readings = self.client.get('/readings/read/meter-100').get_json()
        self.assertIn({"time": 1505825838, "reading": 0.6 }, readings)
        self.assertIn({"time": 1505825848, "reading": 0.65 }, readings)
        self.assertIn({"time": 1605825849, "reading": 0.7}, readings)

    def test_respond_with_error_if_smart_meter_id_not_set(self):
        readingJson = {
            "electricityReadings": [
                { "time": 1505825838, "reading": 0.6 }
            ]
        }

        with self.assertRaises(Exception):
            self.client.post('/readings/store', json=readingJson)

    def test_respond_with_error_if_electricity_readings_not_set(self):
        readingJson = {
            "smartMeterId": "meter-11"
        }

        with self.assertRaises(Exception):
            self.client.post('/readings/store', json=readingJson)
