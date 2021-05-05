from app import app, sign_in_test
import unittest

# Patient id used for testing purposes.
pid = "-MZxdolOqXRO79q_7VwB"
userID = sign_in_test("demo-cardio21@gmail.com", "Cardiodemo100!")

class ContentTest(unittest.TestCase):
    """
    Test the content of the pages when correct and incorrect parameters are passed in.
    """

    # Set up config.
    def setUp(self):
        # Initialize test client.
        self.app = app.test_client()
        app.secret_key = "OMONOIALAOSPROTATHLIMA"
        # Initialise USERID to be used for test purposes.
        

    # Test that "/" - index, loads the correct data.
    def test_index(self):
         with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
            
            # Since user is logged in, it will take them to the patients page.
            response = c.get('/', follow_redirects=True)
            self.assertTrue(b'Patients' in response.data)

    # Test that "diagnose" page, loads the correct data.
    def test_diagnose(self):
         with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/diagnose?pid='+pid, follow_redirects=True)
            self.assertTrue(b"Fill out the form to diagnose whether the patient suffers from a cardiovascular disease." in response.data)

    # Test that if pid is not passed in the "diagnose" page, the "diagnose" page is not loaded.
    def test_diagnose_without_pid(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/diagnose', follow_redirects=True)
            self.assertFalse(b"Fill out the form to diagnose whether the patient suffers from a cardiovascular disease." in response.data)

    # Test that "edit" page, loads the correct data.
    def test_edit(self):
          with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get(
                'edit?pid='+pid, follow_redirects=True)
            self.assertTrue(b"Edit Patient" in response.data)

    # Test that if pid is not passed in the "edit" page, it's not loaded.
    def test_edit_without_pid(self):
         with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/edit', follow_redirects=True)
            self.assertFalse(b"Edit Patient" in response.data)

    # Test that "history" page, loads the correct data.
    def test_history(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get(
            '/history?pid='+pid, follow_redirects=True)
            self.assertTrue(b"View Details" in response.data)

    # Test that if pid is not passed in the "history" page, it's not loaded.
    def test_history_without_pid(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/history', follow_redirects=True)
            self.assertFalse(b"View Details" in response.data)

    # Test that "report" page, doesn't load when data is passed like this without diagnosing first.
    def test_report(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/report?pred=Most+Likely+Healthy&neg=0.82&pos=0.18&pid='+pid+'&ct=1619438610', follow_redirects=True)
            self.assertFalse(b"Most Likely Healthy" in response.data)

    # Test that if pid is not passed in the "report" page, it's not loaded.
    def test_report_without_vars(self):
         with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
                
            response = c.get('/report', follow_redirects=True)
            self.assertFalse(b"Most Likely Healthy" in response.data)


if __name__ == "__main__":
    unittest.main()
