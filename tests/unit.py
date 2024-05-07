import unittest

from flask_testing import TestCase
from main import app

username = 'admin1'
password = "6QhZy+!Gc)5y@g@"

class TestFlaskApp(TestCase):
    

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200) # тест на то, что главная страница существует

    def test_login(self):
        
        response = self.client.post('/login', data=dict(username=username, password=password), follow_redirects=True) # тест на логин, вводим имя и пароль
        self.assertEqual(response.status_code, 200) # сайт возвращает код 200, это значит, что сайт что-то вернул и это "что-то" ожидалось, но не обязательно что мы вошли в аккаунт
        self.assertIn(bytes(username, encoding="utf-8"), response.data) # если среди байтов ответа находим имя пользователя, то всё нормально

    def test_logout(self):
        with self.client.session_transaction() as session:
            session['username'] = username # Самостоятельно добавляем username в куки, чтоб не входить в аккаунт
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200) # сайт возвращает код 200, это значит, что сайт что-то вернул и это "что-то" ожидалось, но не обязательно что мы вышли из аккаунта
        

if __name__ == '__main__':
    unittest.main()
