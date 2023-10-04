import base64
import json
import unittest

from api import app
from models import db

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_auth_header(self, username, password):
        return {
            'Authorization': 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
        }

    def test_get_movies(self):
        response = self.app.get('/movies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('movies', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total_items', data)
        self.assertEqual(len(data['movies']), 10)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['per_page'], 10)

    def test_get_movie(self):
        response = self.app.get('/movies/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('title', data)

    def test_get_non_existing_movie(self):
        response = self.app.get('/movies/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Movie not found')

    def test_get_movie_by_title(self):
        response = self.app.get('/movies/title/Movie 1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('title', data)

    def test_get_movie_by_non_existing_title(self):
        response = self.app.get('/movies/title/Nonexistent Movie')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Movie not found')

    def test_add_movie(self):
        headers = self.get_auth_header('test_user', 'password123')
        data = {'title': 'Test Movie'}
        response = self.app.post('/movies', json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('message', data)

    def test_add_movie_missing_title(self):
        headers = self.get_auth_header('test_user', 'password123')
        data = {}
        response = self.app.post('/movies', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Title is required')

    def test_add_movie_unauthorized(self):
        headers = self.get_auth_header('invalid_user', 'invalid_password')
        data = {'title': 'NewMovieTitle'}
        response = self.app.post('/movies', json=data, headers=headers)
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_remove_movie(self):
        headers = self.get_auth_header('test_user', 'password123')
        response = self.app.delete('/movies/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Movie deleted successfully')

    def test_remove_non_existing_movie(self):
        headers = self.get_auth_header('test_user', 'password123')
        response = self.app.delete('/movies/9999', headers=headers)
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Movie not found')

    def test_remove_movie_unauthorized(self):
        headers = self.get_auth_header('test_user', 'password123')
        response = self.app.delete('/movies/2', headers=headers)
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_invalid_pagination(self):
        response = self.app.get('/movies?page=abc&per_page=xyz')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Invalid page or per_page values')

    def test_custom_pagination(self):
        response = self.app.get('/movies?page=2&per_page=5')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['page'], 2)
        self.assertEqual(data['per_page'], 5)


if __name__ == '__main__':
    unittest.main()
