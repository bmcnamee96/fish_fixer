import http from 'node:http';
import { normalizeCaseInput, buildAssessment } from './diagnosisService.js';

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => {
      raw += chunk;
      if (raw.length > 1_000_000) {
        reject(new Error('Request body too large'));
      }
    });
    req.on('end', () => {
      if (!raw) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(raw));
      } catch (error) {
        reject(new Error('Invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, { 'content-type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

async function handleRequest(req, res) {
  if (req.method === 'GET' && req.url === '/') {
    return sendJson(res, 200, { ok: true, service: 'fish-fixer-api', message: 'Fish Fixer API is running' });
  }

  if (req.method === 'GET' && req.url === '/api/health') {
    return sendJson(res, 200, { ok: true, service: 'fish-fixer-api' });
  }

  if (req.method === 'POST' && req.url === '/api/cases') {
    const body = await readJsonBody(req);
    const normalized = normalizeCaseInput(body);
    const assessment = buildAssessment(normalized);
    return sendJson(res, 200, { case: normalized, assessment });
  }

  if (req.method === 'POST' && req.url === '/api/chat') {
    const body = await readJsonBody(req);
    const message = body.message || 'Please describe your fish symptoms.';
    return sendJson(res, 200, {
      response: `Thanks for the details. Next, share water test values and symptom timeline. (${message})`
    });
  }

  if (req.method === 'POST' && req.url === '/api/photos') {
    return sendJson(res, 501, {
      message: 'Photo processing endpoint scaffolded. Storage integration is next.'
    });
  }

  return sendJson(res, 404, { error: 'Not found' });
}

export function createServer() {
  return http.createServer((req, res) => {
    handleRequest(req, res).catch(error => {
      sendJson(res, 400, { error: error.message });
    });
  });
}

if (process.env.NODE_ENV !== 'test') {
  const port = Number(process.env.PORT || 3001);
  createServer().listen(port, () => {
    console.log(`Fish Fixer API listening on http://localhost:${port}`);
  });
}
