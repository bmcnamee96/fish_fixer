# Fish Fixer App Index

## API (Node)

### File: `apps/api/src/server.js`

- `readJsonBody(req)`
  - Parses JSON request payloads with a body-size guard.
- `sendJson(res, statusCode, payload)`
  - Sends standard JSON responses.
- `handleRequest(req, res)`
  - Routes API requests for:
    - `GET /api/health`
    - `POST /api/cases`
    - `POST /api/chat`
    - `POST /api/photos` (scaffold)
- `createServer()`
  - Creates the HTTP server and central request error handling wrapper.

### File: `apps/api/src/diagnosisService.js`

- `normalizeCaseInput(payload)`
  - Normalizes case inputs (snake_case + camelCase compatibility).
- `buildAssessment(normalizedInput)`
  - Produces a structured assessment shell including alerts and next steps.

### File: `apps/api/src/rules.js`

- `evaluateWaterQuality(observation)`
  - Applies freshwater/saltwater threshold checks for water-quality risk alerts.

## Frontend (React)

### File: `apps/web/src/App.jsx`

- `App()`
  - Root migration scaffold that renders the three core product modes.

### Files: `apps/web/src/components/*.jsx`

- `FormMode()`
  - Structured diagnosis intake mode placeholder.
- `ChatMode()`
  - Conversational diagnosis support mode placeholder.
- `PhotoMode()`
  - Photo upload-assisted mode placeholder.

## Planning and Tests

- `plan.md`
  - React + Node migration plan with architecture, phased implementation, and DoD.
- `tests/test_plan_doc.py`
  - Asserts the migration plan exists and includes core sections.
- `tests/test_node_react_scaffold.py`
  - Verifies scaffold files/endpoints and freshwater/saltwater rule coverage.
