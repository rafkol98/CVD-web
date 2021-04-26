from app import app
import unittest

class FormsTest(unittest.TestCase):
    
    # Set up config.
    def setUp(self):
        self.app = app.test_client()
        app.config['USERID'] = "LAZxVbjxuaYot9WVpMDH2ssYJjA3"

    def test_add_patient(self):
        response = self.app.post(
        '/patients/',
        data=dict(age="24", gender="0", name="Test", lastName="TestLast", email="test@gmail.com"),
        follow_redirects=False
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_patient(self):
        response = self.app.post(
        '/edit?pid=-MZDf5ZX5tR3GoVlllwf',
        data = dict(age=31, gender=0, name="Rafael", lastName="Panikos", email="kokos@gmail.com"),
        follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_diagnose_patient(self):
        response = self.app.post(
        '/diagnose?pid=-MZDf5ZX5tR3GoVlllwf',
        data = dict(chest = 2,
            bps = 170,
            chol = 300, 
            fbs = 0,
            ecg = 1,
            maxheart = 120,
            exang = 1,
            oldpeak = 1.5,
            stslope = 2),
        follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    app.secret_key = 'OMONOIALAOSPROTATHLIMA'
    unittest.main()
    app.run()