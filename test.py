from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
        
    def test_homepage(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("plays"))
            self.assertIn("board", session)
            self.assertIn("<h1>Boggle Board</h1>", html)

    def test_correct_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"],
                                 ["H", "E", "L", "L", "O"]]
            response = client.get("/check-word?word=hello")
            self.assertEqual(response.json['result'], 'ok')

    def test_incorrect_word(self):
        with app.test_client() as client:
            client.get("/")
            response = client.get("/check-word?word=hello")
            self.assertEqual(response.json['result'], 'not-on-board')
    
    def test_not_word(self):
        with app.test_client() as client:
            client.get("/")
            response = client.get("/check-word?word=ghnbhdfj")
            self.assertEqual(response.json['result'], 'not-word')