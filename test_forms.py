from app import app
import unittest

# Patient id used for testing purposes.
pid = "-MWZ3OxxmQoRFayfFbLF"

class FormsTest(unittest.TestCase):
    """
    Test that the forms of the app execute without errors.
    """

    # Set up config.
    def setUp(self):
        self.app = app.test_client()
        app.secret_key = 'OMONOIALAOSPROTATHLIMA'
        app.config['USERID'] = "LAZxVbjxuaYot9WVpMDH2ssYJjA3"

    def test_add_patient(self):
        response = self.app.post(
            '/patients/',
            data=dict(age="24", gender="0", name="Test",
                      lastName="TestLast", email="test@gmail.com"),
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_patient(self):
        response = self.app.post(
            '/edit?pid='+pid,
            data=dict(age=31, gender=0, name="Rafael",
                      lastName="Panikos", email="kokos@gmail.com"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_diagnose_patient(self):
        response = self.app.post(
            '/diagnose?pid='+pid,
            data=dict(chest=2,
                      bps=170,
                      chol=300,
                      fbs=0,
                      ecg=1,
                      maxheart=120,
                      exang=1,
                      oldpeak=1.5,
                      stslope=2),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    app.run()
