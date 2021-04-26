from app import app
import unittest

pid = "-MWZ3OxxmQoRFayfFbLF"
class FlaskTest(unittest.TestCase):

    # Check that "Index" page loads.
    def test_index(self):
        response = app.test_client(self).get('/', follow_redirects=True)
        self.assertTrue(response.status_code, 200)
    
    # Check that "Diagnose" page loads.
    def test_diagnose(self):
        response = app.test_client(self).get('/diagnose', follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    # Check that "Edit" page loads.
    def test_edit(self):
        tester = app.test_client(self)
        response = tester.get("/edit?pid="+pid)
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check that "History" page loads.
    def test_history(self):
        tester = app.test_client(self)
        response = tester.get("/history?pid=-MWZ3OxxmQoRFayfFbLF")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check that "Patients" page loads.
    def test_patients(self):
        tester = app.test_client(self)
        response = tester.get("/patients/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check that a patient is added successfully.
    def test_add_patient_correct(self):
        tester = app.test_client(self)
        response = tester.post('/patients/', data=dict(
                age = "34",
                gender = "1",
                name = "Test",
                lastName = "Test2",
                email = "test@test.com"))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)



    

if __name__ == "__main__":
    unittest.main()