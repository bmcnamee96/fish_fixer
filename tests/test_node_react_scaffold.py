from pathlib import Path


def test_scaffold_files_exist():
    required = [
        'package.json',
        'apps/api/src/server.js',
        'apps/api/src/diagnosisService.js',
        'apps/api/src/rules.js',
        'apps/web/src/App.jsx',
        'apps/web/src/components/FormMode.jsx',
        'apps/web/src/components/ChatMode.jsx',
        'apps/web/src/components/PhotoMode.jsx',
    ]
    for rel in required:
        assert Path(rel).exists(), f'Missing scaffold file: {rel}'


def test_api_endpoints_scaffolded():
    content = Path('apps/api/src/server.js').read_text(encoding='utf-8')
    for endpoint in ['/api/health', '/api/cases', '/api/chat', '/api/photos']:
        assert endpoint in content


def test_rules_include_fresh_and_saltwater_logic():
    content = Path('apps/api/src/rules.js').read_text(encoding='utf-8').lower()
    assert 'freshwater' in content
    assert 'saltwater' in content
