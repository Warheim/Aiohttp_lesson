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


def test_create_user():
    response = requests.post(f'{API_URL}/users/', json={'name': 'test_user', 'password': '123'})
    assert response.status_code == 200
    user_data = response.json()
    assert 'id' in user_data
    assert isinstance(user_data['id'], int)


def test_create_existing_user():
    response = requests.post(f'{API_URL}/users/', json={'name': 'test_user', 'password': '123'})
    assert response.status_code == 409
    assert response.json() == {'description': 'user already exists', 'status': 'error'}


def test_patch_user(create_user):
    user_id = create_user['id']
    response = requests.patch(f'{API_URL}/users/{user_id}', json={'name': 'patched_user'})
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}
    response = requests.get(f'{API_URL}/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'patched_user'


def test_user_delete(create_user):
    user_id = create_user['id']
    response = requests.delete(f'{API_URL}/users/{user_id}')
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}
    response = requests.get(f'{API_URL}/users/{user_id}')
    assert response.status_code == 404
    assert response.json() == {'status': 'error', 'description': 'user not found'}
