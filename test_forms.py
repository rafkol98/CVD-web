from app import app, sign_in_test
import os
import unittest

# Patient id used for testing purposes.
pid = "-MZxdolOqXRO79q_7VwB"
userID = sign_in_test("demo-cardio21@gmail.com", "Cardiodemo100!")

class FormsTest(unittest.TestCase):
    """
    Test that the forms of the app execute without errors.
    """

    # Set up config.
    def setUp(self):
        self.app = app.test_client()
        app.secret_key = "OMONOIALAOSPROTATHLIMA"

    def test_add_patient(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID

            response = c.post(
                '/patients/',
                data=dict(age="24", gender="0"),
                follow_redirects=True
            )
            
            self.assertEqual(response.status_code, 200)

    def test_edit_patient(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID

            response = c.post(
                '/edit?pid='+pid,
                data=dict(age=31, gender=0),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

    def test_diagnose_patient(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['usr'] = userID
            response = c.post(
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
