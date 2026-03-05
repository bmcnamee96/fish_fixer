import json
from pathlib import Path


def test_root_package_has_start_script_for_heroku():
    package = json.loads(Path('package.json').read_text(encoding='utf-8'))
    assert 'scripts' in package
    assert package['scripts'].get('start') == 'node apps/api/src/server.js'


def test_procfile_uses_npm_start():
    procfile = Path('Procfile').read_text(encoding='utf-8').strip()
    assert procfile == 'web: npm start'


def test_server_has_root_route():
    server = Path('apps/api/src/server.js').read_text(encoding='utf-8')
    assert "req.method === 'GET' && req.url === '/'" in server
