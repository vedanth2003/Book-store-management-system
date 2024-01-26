import unittest
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_endpoint(self):
        response = requests.get('http://localhost:5000/')
        self.assertEqual(response.status_code, 200)

    def test_add_endpoint(self):
        book_data = {'title': 'New Book', 'author': 'New Author'}
        response = requests.post('http://localhost:5000/add', data=book_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful POST

    def test_edit_rating_endpoint(self):
        book_data = {'id': 1, 'rating': 5}  # Assuming book with ID 1 exists
        response = requests.post('http://localhost:5000/edit-rating', data=book_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful POST

    def test_delete_endpoint(self):
        params = {'id': 1}  # Assuming book with ID 1 exists
        response = requests.get('http://localhost:5000/delete', params=params)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful GET

if __name__ == '__main__':
    unittest.main()
