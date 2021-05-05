from app import app
import os
import unittest

pid = "-MWZ3OxxmQoRFayfFbLF"


class FlaskTest(unittest.TestCase):
    """
    Test that the pages of the app load without errors.
    """

    # Set up config.
    def setUp(self):
        # Initialize test client.
        app.secret_key = "OMONOIALAOSPROTATHLIMA"
        self.app = app.test_client()
        # Initialise USERID to be used for test purposes.
        app.config['USERID'] = "LAZxVbjxuaYot9WVpMDH2ssYJjA3"

    # Check that "Index" page loads.
    def test_index(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    # Check that "Diagnose" page loads.
    def test_diagnose(self):
        response = self.app.get('/diagnose', follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    # Check that "Edit" page loads.
    def test_edit(self):
        response = self.app.get("/edit?pid="+pid)
        self.assertEqual(response.status_code, 200)

    # Check that "History" page loads.
    def test_history(self):
        response = self.app.get("/history?pid="+pid)
        self.assertEqual(response.status_code, 200)

    # Check that "Patients" page loads.
    def test_patients(self):
        response = self.app.get("/patients/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
