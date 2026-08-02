import pytest

from src.app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_demo_login_and_dashboard_endpoints_work(client):
    login_response = client.post(
        '/api/v1/auth/login',
        json={'email': 'admin@hrms.local', 'password': 'Demo@1234'},
    )
    assert login_response.status_code == 200

    employees_response = client.get('/api/v1/employees')
    assert employees_response.status_code == 200
    payload = employees_response.get_json()
    assert 'employees' in payload

    dashboard_response = client.get('/api/v1/dashboard/stats')
    assert dashboard_response.status_code == 200
    stats = dashboard_response.get_json()
    assert stats['total_employees'] >= 0
    assert 'attendance_chart' in stats
