from app import app, sign_in_test
import unittest

# Patient id used for testing purposes.
pid = "-MZxdolOqXRO79q_7VwB"
userID = sign_in_test("demo-cardio21@gmail.com", "Cardiodemo100!")

class FlaskTest(unittest.TestCase):
    """
    Test that the pages of the app load without errors.
    """

    # Set up config.
    def setUp(self):
        # Initialize test client.
        app.secret_key = "OMONOIALAOSPROTATHLIMA"
        self.app = app.test_client()


    # Check that "Index" page loads.
    def test_index(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/', follow_redirects=True)
            self.assertTrue(response.status_code, 200)

    # Check that "Diagnose" page loads.
    def test_diagnose(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/diagnose', follow_redirects=True)
            self.assertTrue(response.status_code, 200)

    # Check that "Edit" page loads.
    def test_edit(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get("/edit?pid="+pid)
            self.assertEqual(response.status_code, 200)

    # Check that "History" page loads.
    def test_history(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get("/history?pid="+pid)
            self.assertEqual(response.status_code, 200)

    # Check that "Patients" page loads.
    def test_patients(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get("/patients/")
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
