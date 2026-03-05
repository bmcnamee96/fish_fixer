# Fish Fixer App Index

## Backend (Flask)

### File: `project_directory/app.py`

- `use_service()` (`POST /use_service`)
  - Receives form submission and optional photo upload.
  - Collects multi-select symptoms, saves uploaded image to `project_directory/uploads/`, builds LLM prompt, and returns diagnosis JSON.

- `system_message()`
  - Returns the system prompt template that instructs the model how to format diagnosis output.

- `generate_prompt(data)`
  - Normalizes incoming form fields, removes empty values, and composes a structured fish-health prompt sent to the model.

- `subscribe()` (`POST /subscribe`)
  - Placeholder endpoint for subscription flow (currently returns success without persistence).

- `index()` (`GET /`)
  - Serves the frontend entry page `project_directory/static/index.html`.

## Frontend (Static)

### Page: `project_directory/static/index.html`

- Landing page and primary UI for Fish Fixer.
- Contains:
  - “Diagnose Your Fish” CTA.
  - Multi-section diagnosis form (details, symptoms, water quality, environment, history, photo upload).
  - Loading spinner and diagnosis response modal.
  - Support/Donation section and disclaimer.

### Script: `project_directory/static/app.js`

- `checkFreeUses()`
  - Tracks client-side free usage attempts via `localStorage` and gates access to the form.

- `showForm()` / `hideForm()`
  - Toggles diagnosis form visibility.

- `showSpinner()` / `hideSpinner()`
  - Controls loading spinner visibility during request lifecycle.

- `formatContent(content)`
  - Wraps returned diagnosis HTML content for modal presentation.

- `showModal(responseText)`
  - Applies lightweight markdown-style formatting to response and shows modal.

- `convertFileToBase64(file, callback)`
  - Converts a selected file to base64 (helper; not currently used in active request flow).

- `displayImage(base64String)`
  - Appends an image to the page from base64 input (helper/debug utility).

- `submitForm(event)`
  - Intercepts form submit, builds `FormData`, includes photo, sends `POST /use_service`, handles response/error, and updates UI.

- `closeModal()`
  - Hides diagnosis modal safely.

### Styles: `project_directory/static/styles.css`

- Styles landing layout, form sections, buttons, spinner, modal, and footer/support blocks.

## Runtime/Entry

- `project_directory/Procfile`
  - Process entry: `web: python app.py`.

## Planning and Quality Docs

- `plan.md`
  - Migration roadmap for fully transitioning Fish Fixer to React + Node, including architecture, phases, and definition of done.

- `tests/test_plan_doc.py`
  - Basic documentation tests to ensure `plan.md` exists and contains core migration sections.

## React + Node Migration Scaffold

### API: `apps/api/src/server.js`

- `readJsonBody(req)`
  - Reads and parses JSON request bodies with a basic size limit.
- `sendJson(res, statusCode, payload)`
  - Sends JSON responses with consistent content type.
- `handleRequest(req, res)`
  - Routes API requests for `/api/health`, `/api/cases`, `/api/chat`, and `/api/photos`.
- `createServer()`
  - Creates the Node HTTP server and centralizes async error handling.

### API domain: `apps/api/src/diagnosisService.js`

- `normalizeCaseInput(payload)`
  - Normalizes snake_case/camelCase case fields for consistent backend processing.
- `buildAssessment(normalizedInput)`
  - Builds a structured scaffold assessment and safe next-step guidance.

### API rules: `apps/api/src/rules.js`

- `evaluateWaterQuality(observation)`
  - Applies freshwater/saltwater water-quality threshold checks and returns safety alerts.

### React app: `apps/web/src/App.jsx`

- `App()`
  - Root React migration scaffold that renders form/chat/photo mode sections.

### React components: `apps/web/src/components/*.jsx`

- `FormMode()`
  - Placeholder section for structured fish diagnosis intake flow.
- `ChatMode()`
  - Placeholder section for conversational fish-health Q&A flow.
- `PhotoMode()`
  - Placeholder section for image upload-assisted analysis flow.

### Tests

- `tests/test_node_react_scaffold.py`
  - Validates migration scaffold structure and API endpoint scaffolding contracts.
