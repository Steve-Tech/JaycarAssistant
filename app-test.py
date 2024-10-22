import unittest

from app import app
import data_file


class PageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def testPages(self):
        # Test pages
        for page in ['/', '/resistors', '/capacitors_e', '/capacitors_o', '/pots']:
            self.assertEqual(self.app.get(page, follow_redirects=True).status_code, 200)
        # Test pages with known values
        for page in ['/resistors?value=100K', '/capacitors_e?value=470N&volts=63', '/capacitors_o?value=10N&volts=100', '/pots?value=10K&type=A']:
            self.assertEqual(self.app.get(page, follow_redirects=True).status_code, 200)
        # Test pages with unknown values
        for page in ['/resistors?value=101K', '/capacitors_e?value=471N&volts=64', '/capacitors_o?value=11N&volts=101', '/pots?value=11K&type=A']:
            self.assertEqual(self.app.get(page, follow_redirects=True).status_code, 200)
        # Test pages with bad values
        for page in ['/resistors?value=100A', '/capacitors_e?value=470A&volts=64', '/capacitors_o?value=10A&volts=101', '/pots?value=10A&type=A']:
            self.assertEqual(self.app.get(page, follow_redirects=True).status_code, 400)
        # Test page not found
        self.assertEqual(self.app.get('/404', follow_redirects=True).status_code, 404)


class CSVTest(unittest.TestCase):
    def testFiles(self):
        for fileName in ['Resistors.csv', 'Potentiometers.csv', 'Capacitors.csv', 'CapacitorsE.csv']:
            self.assertIsNotNone(data_file.openCSV(fileName))

    def testTables(self):
        self.assertIsNotNone(data_file.Resistors.table)
        self.assertIsNotNone(data_file.Potentiometers.table)
        self.assertIsNotNone(data_file.Capacitors.table)
        self.assertIsNotNone(data_file.CapacitorsE.table)


if __name__ == '__main__':
    unittest.main()
