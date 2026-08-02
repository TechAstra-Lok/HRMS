from src.app import app

client = app.test_client()
resp = client.post('/api/v1/auth/login', json={'email': 'admin@hrms.local', 'password': 'Demo@1234'})
print('login', resp.status_code, resp.get_json())
emp = client.get('/api/v1/employees')
print('employees', emp.status_code, emp.get_json())
stats = client.get('/api/v1/dashboard/stats')
print('stats', stats.status_code, stats.get_json())
