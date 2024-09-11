import unittest
from app import app, db, User
from flask import json

class UserTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        response = self.app.post('/users', json={
            'nombres': 'John',
            'apellidos': 'Doe',
            'fecha_nacimiento': '1990-01-01',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User created', response.data)

    def test_get_users(self):
        self.app.post('/users', json={
            'nombres': 'Jane',
            'apellidos': 'Doe',
            'fecha_nacimiento': '1995-05-05',
            'password': 'password123'
        })

        response = self.app.get('/users')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombres'], 'Jane')

    def test_missing_field(self):
        response = self.app.post('/users', json={
            'nombres': 'John',
            'apellidos': '',
            'fecha_nacimiento': '1990-01-01',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Field missing', response.data)

