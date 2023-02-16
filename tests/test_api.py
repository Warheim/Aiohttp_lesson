import requests

API_URL = 'http://127.0.0.1:8000'


def test_user_not_exist():
    response = requests.get(f'{API_URL}/users/999999999')
    assert response.status_code == 404
    assert response.json() == {'status': 'error', 'description': 'user not found'}


def test_user_exist(create_user):
    user_id = create_user.get('id')
    response = requests.get(f'{API_URL}/users/{user_id}')
    assert response.status_code == 200
    user = response.json()
    assert create_user['name'] == user['name']