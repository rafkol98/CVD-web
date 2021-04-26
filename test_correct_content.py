from app import app
import unittest

class ContentTest(unittest.TestCase):

    # Set up config.
    def setUp(self):
        app.config['USERID'] = "LAZxVbjxuaYot9WVpMDH2ssYJjA3"

    # Test that "/" - index, loads the correct data.
    def test_index(self):
        response = app.test_client(self).get('/', follow_redirects=True)
        self.assertTrue(b'About' in response.data)
    
    # Test that "diagnose" page, loads the correct data.
    def test_diagnose(self):
        response = app.test_client(self).get('/diagnose?pid=-MYyrznVMeitn--ovNEJ', follow_redirects=True)
        self.assertTrue(b"Fill out the form to diagnose whether the patient suffers from a cardiovascular disease." in response.data)
    
    # Test that if pid is not passed in the "diagnose" page, the "diagnose" page is not loaded.
    def test_diagnose_without_pid(self):
        response = app.test_client(self).get('/diagnose', follow_redirects=True)
        self.assertFalse(b"Fill out the form to diagnose whether the patient suffers from a cardiovascular disease." in response.data)

    # Test that "edit" page, loads the correct data.
    def test_edit(self):
        response = app.test_client(self).get('/edit?pid=-MYyrznVMeitn--ovNEJ', follow_redirects=True)
        self.assertTrue(b"Edit Patient" in response.data)

    # Test that if pid is not passed in the "edit" page, it's not loaded.
    def test_edit_without_pid(self):
        response = app.test_client(self).get('/edit', follow_redirects=True)
        self.assertFalse(b"Edit Patient" in response.data)

    # Test that "history" page, loads the correct data.
    def test_history(self):
        response = app.test_client(self).get('/history?pid=-MYyrznVMeitn--ovNEJ', follow_redirects=True)
        self.assertTrue(b"History" in response.data)

    # Test that if pid is not passed in the "history" page, it's not loaded.
    def test_history_without_pid(self):
        response = app.test_client(self).get('/history', follow_redirects=True)
        self.assertFalse(b"History" in response.data)

    # Test that "report" page, loads the correct data.
    def test_report(self):
        response = app.test_client(self).get('/report?pred=Most+Likely+Healthy&neg=0.82&pos=0.18&pid=-MYyrznVMeitn--ovNEJ&ct=1619438610', follow_redirects=True)
        self.assertTrue(b"Most Likely Healthy" in response.data)

    # Test that if pid is not passed in the "report" page, it's not loaded.
    def test_report_without_vars(self):
        response = app.test_client(self).get('/report', follow_redirects=True)
        self.assertFalse(b"Most Likely Healthy" in response.data)




if __name__ == "__main__":
    unittest.main()