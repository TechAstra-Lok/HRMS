import sys
sys.path.insert(0, '.')
import app

client = app.app.test_client()
resp = client.post('/api/v1/auth/login', json={'email': 'admin@hrms.local', 'password': 'Demo@1234'})
print(resp.status_code)
print(resp.get_data(as_text=True))
