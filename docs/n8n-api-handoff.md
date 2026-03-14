# n8n → Backend API Handoff

**Backend base URL (Railway):**  
`https://podium-hackathon-2026-production.up.railway.app`

All endpoints below are relative to this base. Use **JSON** for request bodies and `Content-Type: application/json`.

---

## 1. Start a demo run (call first)

When the workflow is triggered with **one business URL**, n8n should call this once at the very start so the dashboard can show the pipeline and target.

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `https://podium-hackathon-2026-production.up.railway.app/api/demo/start` |
| **Body** | `{ "url": "https://the-business-website.com" }` |
| **Response** | `{ "ok": true, "target_url": "https://..." }` |

---

## 2. Report each pipeline step (call after each of the 5 steps)

After **each** of the five steps (Discovery → Assessment → Build → Deploy → Email), n8n should call this so the frontend can show progress and artifacts.

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `https://podium-hackathon-2026-production.up.railway.app/api/pipeline-step` |
| **Body** | See below |

**Request body shape:**

```json
{
  "step": "discovery" | "assessment" | "build" | "deploy" | "email",
  "status": "running" | "done" | "error",
  "error": "optional; only when status is \"error\"",
  "payload": { }
}
```

**When to send:**

- **Start of a step:** `{ "step": "discovery", "status": "running" }` (no payload needed).
- **Step finished successfully:** `{ "step": "discovery", "status": "done", "payload": { ... } }`.
- **Step failed:** `{ "step": "discovery", "status": "error", "error": "Short message" }`.

**Payload by step (when `status` is `"done"`):**

| Step | Suggested `payload` | What the dashboard shows |
|------|---------------------|---------------------------|
| **discovery** | `{ "brand_profile": { "company_name", "primary_color", "secondary_color", "value_proposition", "contact_email", ... } }` | Brand summary |
| **assessment** | `{ "opportunity_report": { "opportunities": [ { "name", "impact", "description" }, ... ] } }` | List of opportunities |
| **build** | `{ }` or e.g. `{ "generated_lp_url": "..." }` | (Optional) Build done |
| **deploy** | `{ "deployed_url": "https://xxx.vercel.app/..." }` | **Live Vercel URL** (clickable) |
| **email** | `{ "outreach_email": { "to", "subject", "body", "sent_at" } }` | “Email sent” + content |

**Example – start Discovery:**  
`POST /api/pipeline-step`  
`{ "step": "discovery", "status": "running" }`

**Example – Discovery done (with brand from your node):**  
`POST /api/pipeline-step`  
`{ "step": "discovery", "status": "done", "payload": { "brand_profile": { "company_name": "Joe's Pizza", "primary_color": "#e94560", "value_proposition": "Best pizza in town", "contact_email": "joe@example.com", ... } } }`

**Example – Deploy done (Vercel URL):**  
`POST /api/pipeline-step`  
`{ "step": "deploy", "status": "done", "payload": { "deployed_url": "https://apex-demo-xyz.vercel.app" } }`

**Example – Email done:**  
`POST /api/pipeline-step`  
`{ "step": "email", "status": "done", "payload": { "outreach_email": { "to": "joe@example.com", "subject": "...", "body": "...", "sent_at": "2026-03-14T20:00:00.000Z" } } }`

**Response:**  
`{ "ok": true, "step": "discovery", "status": "done" }`

---

## 3. Optional: Run Discovery on the backend (if n8n wants backend to do Discovery)

If you prefer the **backend** to run the Discovery Agent (fetch URL + Claude brand extraction) instead of doing it in n8n:

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `https://podium-hackathon-2026-production.up.railway.app/api/discovery` |
| **Body** | `{ "url": "https://..." }` or `{ "url": "https://...", "html": "<html>...</html>" }` (use `html` when the site is hard to fetch) |
| **Response** | `{ "ok": true, "brand_profile": { ... } }` |

n8n can then use `brand_profile` in the workflow and/or send it in the **discovery** `payload` when calling `POST /api/pipeline-step`.

---

## 4. Optional: Backend composes and “sends” the outreach email

If you want the **backend** to generate the email (Claude) and record it as sent (no real SMTP):

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `https://podium-hackathon-2026-production.up.railway.app/api/outreach` |
| **Body** | `{ "url": "https://...", "company_name": "optional", "lp_url": "https://xxx.vercel.app" }` |
| **Response** | `{ "ok": true, "sent": true, "email": { "to", "subject", "body", "sent_at", "company_name", "url" } }` |

n8n can call this at the Email step, then report the same email in **email** `payload` via `POST /api/pipeline-step` so the dashboard shows it.

---

## 5. Read state (for debugging; frontend polls this)

The dashboard polls this to show the pipeline strip and artifacts. n8n does **not** need to call it.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `https://podium-hackathon-2026-production.up.railway.app/api/state` |
| **Response** | Full pipeline state: `stage`, `target_url`, `steps`, `brand_profile`, `opportunity_report`, `deployed_url`, `outreach_email`, etc. |

---

## 6. Health check

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `https://podium-hackathon-2026-production.up.railway.app/api/health` |
| **Response** | `{ "status": "ok" }` |

---

## Suggested n8n flow (one-URL demo)

1. **Trigger:** Webhook or manual run with input `{ "url": "https://one-business.com" }`.
2. **First node:** HTTP Request → `POST {{baseUrl}}/api/demo/start` with body `{ "url": "{{ $json.url }}" }`.
3. **Discovery:** Run your Discovery/scrape logic. Then HTTP Request → `POST {{baseUrl}}/api/pipeline-step` with `{ "step": "discovery", "status": "running" }`, then after work is done → `POST /api/pipeline-step` with `{ "step": "discovery", "status": "done", "payload": { "brand_profile": ... } }`.  
   - Or call `POST /api/discovery` and then report done with that `brand_profile` in `payload`.
4. **Assessment:** Same idea: `running` → do work → `done` with `payload: { "opportunity_report": ... }`.
5. **Build:** `running` → generate LP → `done` (optional payload).
6. **Deploy:** `running` → deploy to Vercel → `done` with `payload: { "deployed_url": "https://..." }`.
7. **Email:** `running` → send email (via backend `POST /api/outreach` and/or your SMTP) → `done` with `payload: { "outreach_email": { "to", "subject", "body", "sent_at" } }`.

**Base URL to paste in n8n:**  
`https://podium-hackathon-2026-production.up.railway.app`

No API keys required for these endpoints; the backend uses its own `ANTHROPIC_API_KEY` for Discovery/Outreach when you call them.
