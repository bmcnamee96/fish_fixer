# Fish Fixer Full Migration Plan (React + Node)

## 1) Goals

- Fully replace the current Flask + static frontend app with a modern React + Node stack.
- Support three user workflows from day one:
  1. Structured diagnosis form
  2. Chat / question mode
  3. Photo upload-assisted analysis
- Support both freshwater and saltwater cases with clear and safe guidance.
- Keep AI-driven diagnosis support while adding deterministic safety checks.

---

## 2) Recommended Target Stack

### Frontend
- **React + TypeScript** (Next.js App Router preferred)
- UI library: Tailwind CSS + component kit (shadcn/ui or similar)
- Data fetching: React Query (or Next server actions where appropriate)

### Backend
- **Node.js + TypeScript**
- Framework: **NestJS** (structured, scalable) or Express/Fastify (lighter)
- Validation: Zod or class-validator
- File uploads: Multer (or Next route handlers + S3 SDK)

### Data + Infra
- Database: PostgreSQL
- ORM: Prisma
- File storage: S3-compatible bucket (AWS S3, R2, Supabase Storage)
- Queue/background jobs (later): BullMQ + Redis (image enrichment, async analysis)

### AI Layer
- OpenAI API for language reasoning and multimodal analysis
- Deterministic rules engine for hard safety checks and water-parameter alerts

---

## 3) High-Level Architecture

- `apps/web` (React UI)
- `apps/api` (Node backend)
- `packages/shared` (shared types, schemas, constants)

Core domain objects:
- **Case**: user submission (form/chat/photo context)
- **Observation**: symptoms, behavior, water params
- **Assessment**: ranked possible conditions + confidence + rationale
- **Recommendation**: treatment and non-medication actions + warnings

---

## 4) Product Flows to Implement

### A) Form Diagnosis Mode
1. User submits species, water type, symptoms, water parameters, environment/history.
2. Backend validates and normalizes data.
3. Rules engine flags urgent water-quality issues.
4. LLM generates differential diagnosis + action plan in strict JSON schema.
5. UI displays:
   - likely conditions (ranked)
   - confidence and uncertainty
   - treatment suggestions and monitoring steps
   - emergency escalation guidance

### B) Chat / Question Mode
1. User asks free-form questions.
2. Backend attaches case context (if available).
3. Model answers with fish-health bounded policy and references to known checks.
4. User can promote chat findings into a structured case.

### C) Photo-Assisted Mode
1. User uploads fish image(s).
2. Backend validates size/type, stores in object storage.
3. Image analysis is treated as supporting evidence, not sole diagnosis.
4. Combined output merges visual clues + water/symptom context.

---

## 5) Safety + Quality Guardrails

- Never present output as definitive veterinary diagnosis.
- Always include uncertainty + when to consult aquatic vet.
- Enforce hard guardrails for dangerous water values (ammonia/nitrite/oxygen/temp).
- Block unsafe medication claims when required context (tank size, species sensitivity) is missing.
- Add output schema validation before sending response to client.

---

## 6) API Contract (Initial)

- `POST /api/cases`  
  Create or analyze a structured case from form data.

- `POST /api/chat`  
  Chat response endpoint with optional case context.

- `POST /api/photos`  
  Upload photos and return storage references + optional analysis job state.

- `GET /api/cases/:id`  
  Retrieve prior case and analysis output.

- `POST /api/cases/:id/feedback`  
  Capture user-reported outcome for future quality improvements.

---

## 7) Database Model (MVP)

- `users` (optional initially for anonymous mode)
- `cases`
- `case_observations`
- `case_images`
- `assessments`
- `recommendations`
- `feedback_events`

Store both:
- normalized structured fields, and
- model response payloads (versioned) for audit/debug.

---

## 8) Testing Strategy (Required)

### Unit tests
- Field normalization and schema validation
- Rules engine thresholds and alerts
- Prompt/context builder behavior

### Integration tests
- `/api/cases` happy path + validation failures
- `/api/chat` bounded-response policy checks
- photo upload validation and storage behavior

### End-to-end tests
- Form submit -> diagnosis render
- Chat session -> actionable response
- Photo upload -> analysis shown in UI

### Non-functional checks
- Basic rate limiting tests
- Error handling tests (no raw stack trace leakage)

---

## 9) Migration Execution Plan (Phased)

### Phase 0: Foundation (Week 1)
- Initialize monorepo (pnpm/turborepo recommended).
- Create React app + Node API service.
- Set up CI, linting, formatting, and test pipelines.
- Define shared TypeScript schemas.

### Phase 1: Form Flow Parity (Week 2)
- Implement `POST /api/cases` with validation + stubbed analysis.
- Build React form UI with existing fields from current app.
- Return structured mock assessment; render in new diagnosis UI.

### Phase 2: AI Integration + Rules (Week 3)
- Add OpenAI integration with strict JSON schema outputs.
- Implement water-parameter rules engine.
- Merge rules + LLM into final response contract.

### Phase 3: Chat Mode (Week 4)
- Build chat UI and `POST /api/chat`.
- Add context memory for current case.
- Add policy guardrails and response formatter.

### Phase 4: Photo Mode (Week 5)
- Add secure upload flow and object storage integration.
- Add photo-assisted analysis path.
- Surface visual-confidence notes in results.

### Phase 5: Hardening + Launch Prep (Week 6)
- Add auth/subscription scaffolding (if needed).
- Rate limiting, monitoring, and logging.
- Complete E2E tests and UX polish.
- Decommission Flask/static app from repo.

---

## 10) Definition of Done

- React app is primary UI and Node API is sole backend.
- Form/chat/photo modes all functional in production-ready architecture.
- Freshwater and saltwater checks implemented in deterministic rules layer.
- AI output follows strict schema with safety messaging.
- Test suite covers unit + integration + core E2E flows.
- Legacy Python/Flask app removed.

---

## 11) Immediate Next Actions

1. Approve stack choice: **Next.js + Node/Nest + PostgreSQL + Prisma**.
2. Decide auth at MVP: anonymous first or account-required.
3. Approve initial condition list and safety thresholds.
4. Start Phase 0 repo scaffold and CI setup.
