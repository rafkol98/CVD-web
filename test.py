from app import app
import unittest

class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_diagnose(self):
        tester = app.test_client(self)
        response = tester.get("/diagnose?pid=-MWZ3OxxmQoRFayfFbLF")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_edit(self):
        tester = app.test_client(self)
        response = tester.get("/edit?uid=qr34AfcGffe1rSFrz4JtUzuEYWj2&pid=-MWZ3OxxmQoRFayfFbLF")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_history(self):
        tester = app.test_client(self)
        response = tester.get("/history?uid=qr34AfcGffe1rSFrz4JtUzuEYWj2&pid=-MWZ3OxxmQoRFayfFbLF")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Test that the patient's page is returned correctly.
    def test_patients(self):
        tester = app.test_client(self)
        response = tester.get("/patients")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

   def test_report(self):
        tester = app.test_client(self)
        response = tester.get("/history?uid=qr34AfcGffe1rSFrz4JtUzuEYWj2&pid=-MWZ3OxxmQoRFayfFbLF")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    

if __name__ == "__main__":
    unittest.main()