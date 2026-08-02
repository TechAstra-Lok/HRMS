from src.app import app
import os
print('app.root_path=', app.root_path)
print('resolved data file=', os.path.abspath(os.path.join(app.root_path, '..', '..', 'data', 'employees.json')))
print('exists=', os.path.exists(os.path.abspath(os.path.join(app.root_path, '..', '..', 'data', 'employees.json'))))
