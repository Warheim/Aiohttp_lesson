import requests

API_URL = 'http://127.0.0.1:8000'


def test_root():
    assert requests.get(API_URL).status_code == 404


def test_api():
    response = requests.post(f'{API_URL}/hello_world', headers={'token': '120290'}, json={'my_js': 'your_js'},
                             params={'my_params': 'your params'})
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}
