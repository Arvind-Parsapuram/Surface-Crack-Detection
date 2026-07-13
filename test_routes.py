import sys, threading, time, urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from app import fastapi_app, SPAWrapper

def run():
    wrapped = SPAWrapper(fastapi_app)
    uvicorn.run(wrapped, host='127.0.0.1', port=18901, log_level='error')

t = threading.Thread(target=run, daemon=True)
t.start()
time.sleep(3)

results = {}
for path in ['/', '/dashboard', '/predict', '/user', '/about', '/login', '/register', '/forgot', '/logout', '/nonexistent']:
    try:
        r = urllib.request.urlopen(f'http://127.0.0.1:18901{path}')
        results[path] = f"status={r.status}, len={len(r.read())}"
    except urllib.error.HTTPError as e:
        results[path] = f"status={e.code}"

for path, result in results.items():
    print(f'{path} -> {result}')
print('Done')