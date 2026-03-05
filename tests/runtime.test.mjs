import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';

const read = rel => readFileSync(new URL(`../${rel}`, import.meta.url), 'utf-8');

test('root package has start script for heroku', () => {
  const pkg = JSON.parse(read('package.json'));
  assert.equal(pkg.scripts?.start, 'node apps/api/src/server.js');
});

test('procfile uses npm start', () => {
  assert.equal(read('Procfile').trim(), 'web: npm start');
});

test('server has root route and landing html marker', () => {
  const server = read('apps/api/src/server.js');
  assert.match(server, /req\.method === 'GET' && req\.url === '\/'/);
  assert.match(server, /Fish Fixer API is running/);
  assert.match(server, /sendHtml/);
});

test('node/react scaffold files exist', () => {
  const required = [
    'package.json',
    'apps/api/src/server.js',
    'apps/api/src/diagnosisService.js',
    'apps/api/src/rules.js',
    'apps/web/src/App.jsx',
    'apps/web/src/components/FormMode.jsx',
    'apps/web/src/components/ChatMode.jsx',
    'apps/web/src/components/PhotoMode.jsx'
  ];

  for (const rel of required) {
    assert.equal(existsSync(new URL(`../${rel}`, import.meta.url)), true, `Missing scaffold file: ${rel}`);
  }
});

test('api endpoint routes are scaffolded', () => {
  const server = read('apps/api/src/server.js');
  for (const endpoint of ['/api/health', '/api/cases', '/api/chat', '/api/photos']) {
    assert.match(server, new RegExp(endpoint.replace('/', '\\/')));
  }
});

test('rules include fresh and saltwater logic', () => {
  const rules = read('apps/api/src/rules.js').toLowerCase();
  assert.match(rules, /freshwater/);
  assert.match(rules, /saltwater/);
});

test('migration plan exists and contains required sections', () => {
  assert.equal(existsSync(new URL('../plan.md', import.meta.url)), true);
  const plan = read('plan.md');
  for (const section of ['## 1) Goals', '## 2) Recommended Target Stack', '## 8) Testing Strategy', '## 9) Migration Execution Plan']) {
    assert.equal(plan.includes(section), true, `Missing plan section: ${section}`);
  }
});

test('legacy flask and scratch scripts are removed', () => {
  assert.equal(existsSync(new URL('../project_directory', import.meta.url)), false);
  assert.equal(existsSync(new URL('../input.py', import.meta.url)), false);
  assert.equal(existsSync(new URL('../output.py', import.meta.url)), false);
});
