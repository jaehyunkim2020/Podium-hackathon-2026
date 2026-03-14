"""
FastAPI app for Apex pipeline. Exposes endpoints for the dashboard and pipeline control.

Run from project root:
  uvicorn backend.main:app --reload
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from datetime import datetime, timezone
from typing import Any, Literal

from backend.models import BrandProfile
from backend.agents.discovery import run_discovery
from backend.agents.outreach import compose_outreach_email

# Project root (parent of backend/). Used to serve static frontend.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_ROOT / "static"

# Five pipeline stages for n8n → backend reporting. Frontend displays these in order.
PIPELINE_STEP_IDS = ("discovery", "assessment", "build", "deploy", "email")


def _initial_steps() -> dict[str, dict[str, Any]]:
    return {step: {"status": "pending", "error": None, "payload": None} for step in PIPELINE_STEP_IDS}


# In-memory pipeline state for the demo. Dashboard polls GET /api/state; n8n calls POST /api/pipeline-step.
pipeline_state = {
    "stage": "idle",
    "target_url": None,
    "brand_profile": None,
    "error": None,
    "outreach_sent": [],
    "run_started_at": None,
    "steps": _initial_steps(),
    # Artifacts n8n can set via pipeline-step payload (frontend can show these)
    "opportunity_report": None,
    "deployed_url": None,
    "outreach_email": None,  # last sent email { to, subject, body, sent_at }
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipeline_state["stage"] = "idle"
    pipeline_state["target_url"] = None
    pipeline_state["brand_profile"] = None
    pipeline_state["error"] = None
    pipeline_state["outreach_sent"] = []
    pipeline_state["run_started_at"] = None
    pipeline_state["steps"] = _initial_steps()
    pipeline_state["opportunity_report"] = None
    pipeline_state["deployed_url"] = None
    pipeline_state["outreach_email"] = None
    yield
    # Shutdown: nothing to do for in-memory state
    pass


app = FastAPI(
    title="Apex Pipeline API",
    description="Backend for Apex autonomous web development agency",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/state")
def get_state():
    """Dashboard polls this to show pipeline status and current outputs."""
    return pipeline_state


class DiscoveryRequest(BaseModel):
    """Optional body for /api/discovery. If html is set, we skip fetching the URL (for demo fallback)."""
    url: str
    html: Optional[str] = None


@app.post("/api/discovery")
def run_discovery_endpoint(url: Optional[str] = None, body: Optional[DiscoveryRequest] = None):
    """
    Run the Discovery Agent. Pass ?url=... or a JSON body { "url": "...", "html": "..." }.
    If html is provided, the URL is not fetched (use for demo when the target site times out or blocks).
    """
    if body is not None:
        url = body.url
        html_override = body.html
    else:
        url = url or ""
        html_override = None
    if not url or not url.strip():
        raise HTTPException(status_code=400, detail="url is required (query or body)")
    pipeline_state["stage"] = "discovery"
    pipeline_state["target_url"] = url
    pipeline_state["error"] = None
    pipeline_state["brand_profile"] = None

    try:
        profile = run_discovery(url, html=html_override)
        pipeline_state["brand_profile"] = profile.model_dump()
        return {"ok": True, "brand_profile": profile.model_dump()}
    except httpx.TimeoutException as e:
        pipeline_state["error"] = str(e)
        pipeline_state["stage"] = "idle"
        raise HTTPException(
            status_code=502,
            detail="Request to the target URL timed out. Try a different site or pass saved HTML in the request body (e.g. {\"url\": \"https://...\", \"html\": \"<html>...\"}) for demo.",
        )
    except httpx.ConnectError as e:
        pipeline_state["error"] = str(e)
        pipeline_state["stage"] = "idle"
        raise HTTPException(
            status_code=502,
            detail="Could not connect to the target URL (SSL or network). Try a different URL or pass saved HTML in the body for demo.",
        )
    except ValueError as e:
        msg = str(e)
        if "ANTHROPIC_API_KEY" in msg or "api_key" in msg.lower():
            pipeline_state["error"] = msg
            pipeline_state["stage"] = "idle"
            raise HTTPException(
                status_code=503,
                detail="Anthropic API key not set. Set ANTHROPIC_API_KEY in your environment and restart the server.",
            )
        pipeline_state["error"] = msg
        pipeline_state["stage"] = "idle"
        raise HTTPException(status_code=502, detail=f"Discovery failed: {msg}")
    except Exception as e:
        pipeline_state["error"] = str(e)
        pipeline_state["stage"] = "idle"
        err_msg = str(e)
        if "api_key" in err_msg.lower() or "auth" in err_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Anthropic API key missing or invalid. Set ANTHROPIC_API_KEY in your environment.",
            )
        raise HTTPException(status_code=502, detail=f"Discovery failed: {e}")


@app.get("/api/health")
def health():
    return {"status": "ok"}


# --- Pipeline strip: n8n calls these so the client can show the 5 stages ---

class DemoStartRequest(BaseModel):
    """Body for POST /api/demo/start. Call at the start of a demo run (e.g. from n8n)."""
    url: str


@app.post("/api/demo/start")
def demo_start(body: DemoStartRequest):
    """
    Start a new pipeline run: set target_url, reset all 5 steps to pending, clear artifacts.
    n8n can call this when the workflow is triggered (e.g. with the one business URL).
    """
    url = (body.url or "").strip()
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
    pipeline_state["target_url"] = url
    pipeline_state["stage"] = "discovery"
    pipeline_state["error"] = None
    pipeline_state["run_started_at"] = datetime.now(timezone.utc).isoformat()
    pipeline_state["steps"] = _initial_steps()
    pipeline_state["brand_profile"] = None
    pipeline_state["opportunity_report"] = None
    pipeline_state["deployed_url"] = None
    pipeline_state["outreach_email"] = None
    return {"ok": True, "target_url": url}


class PipelineStepRequest(BaseModel):
    """Body for POST /api/pipeline-step. n8n calls this after each of the 5 steps."""
    step: Literal["discovery", "assessment", "build", "deploy", "email"]
    status: Literal["running", "done", "error"]
    error: Optional[str] = None
    payload: Optional[dict[str, Any]] = None


@app.post("/api/pipeline-step")
def pipeline_step(body: PipelineStepRequest):
    """
    Report a pipeline step result. n8n calls this at each stage (e.g. after Discovery node,
    after Assessment node, etc.). Updates state so GET /api/state reflects progress for the client.
    """
    if body.step not in PIPELINE_STEP_IDS:
        raise HTTPException(status_code=400, detail=f"step must be one of {PIPELINE_STEP_IDS}")
    steps = pipeline_state.get("steps") or _initial_steps()
    steps[body.step] = {
        "status": body.status,
        "error": body.error,
        "payload": body.payload,
    }
    pipeline_state["steps"] = steps
    pipeline_state["stage"] = body.step if body.status in ("running", "done") else "idle"
    if body.status == "error":
        pipeline_state["error"] = body.error

    # Persist common artifacts from payload so frontend and existing logic can use them
    if body.status == "done" and body.payload:
        p = body.payload
        if body.step == "discovery" and "brand_profile" in p:
            pipeline_state["brand_profile"] = p.get("brand_profile")
        if body.step == "assessment" and "opportunity_report" in p:
            pipeline_state["opportunity_report"] = p.get("opportunity_report")
        if body.step == "deploy" and "deployed_url" in p:
            pipeline_state["deployed_url"] = p.get("deployed_url")
        if body.step == "email" and "outreach_email" in p:
            pipeline_state["outreach_email"] = p.get("outreach_email")

    return {"ok": True, "step": body.step, "status": body.status}


# --- Outreach: compose and "send" email (simulated send for demo) ---

class OutreachRequest(BaseModel):
    """Body for POST /api/outreach. Runs discovery for url if needed, then composes and sends email."""
    url: str
    company_name: Optional[str] = None
    html: Optional[str] = None  # optional demo fallback if live fetch fails
    lp_url: Optional[str] = None  # optional generated LP URL to include in email


@app.post("/api/outreach")
def run_outreach_endpoint(body: OutreachRequest):
    """
    For the given business URL (and optional company name / html): ensure we have a brand profile
    (run discovery if needed), compose a personalized outreach email, then "send" it (stored in state;
    no real SMTP unless you add it). Returns the composed email so the client can show it.
    """
    url = (body.url or "").strip()
    if not url:
        raise HTTPException(status_code=400, detail="url is required")

    pipeline_state["stage"] = "outreach"
    pipeline_state["error"] = None

    profile = pipeline_state.get("brand_profile")
    target_url = pipeline_state.get("target_url")
    if profile is None or target_url != url:
        pipeline_state["target_url"] = url
        pipeline_state["brand_profile"] = None
        try:
            discovered = run_discovery(url, html=body.html)
            profile = discovered.model_dump()
            pipeline_state["brand_profile"] = profile
        except httpx.TimeoutException:
            pipeline_state["stage"] = "idle"
            raise HTTPException(status_code=502, detail="Discovery timed out for this URL. Try passing html in the body for demo.")
        except httpx.ConnectError:
            pipeline_state["stage"] = "idle"
            raise HTTPException(status_code=502, detail="Could not fetch URL. Try passing html in the body for demo.")
        except ValueError as e:
            if "ANTHROPIC_API_KEY" in str(e):
                pipeline_state["stage"] = "idle"
                raise HTTPException(status_code=503, detail="Anthropic API key not set.")
            pipeline_state["stage"] = "idle"
            raise HTTPException(status_code=502, detail=str(e))
        except Exception as e:
            pipeline_state["error"] = str(e)
            pipeline_state["stage"] = "idle"
            raise HTTPException(status_code=502, detail=f"Discovery failed: {e}")

    company_name = body.company_name or profile.get("company_name") or "there"
    value_proposition = profile.get("value_proposition") or "your business"
    contact_email = profile.get("contact_email") or "contact@example.com"

    try:
        subject, body_text = compose_outreach_email(
            company_name=company_name,
            value_proposition=value_proposition,
            contact_email=contact_email,
            lp_url=body.lp_url,
        )
    except ValueError as e:
        pipeline_state["stage"] = "idle"
        if "API key" in str(e):
            raise HTTPException(status_code=503, detail="Anthropic API key not set.")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        pipeline_state["stage"] = "idle"
        raise HTTPException(status_code=502, detail=f"Outreach composition failed: {e}")

    sent_at = datetime.now(timezone.utc).isoformat()
    record = {
        "url": url,
        "company_name": company_name,
        "subject": subject,
        "body": body_text,
        "to": contact_email,
        "sent_at": sent_at,
    }
    pipeline_state["outreach_sent"] = pipeline_state.get("outreach_sent") or []
    pipeline_state["outreach_sent"].append(record)
    pipeline_state["stage"] = "idle"

    return {
        "ok": True,
        "sent": True,
        "email": {
            "subject": subject,
            "body": body_text,
            "to": contact_email,
            "sent_at": sent_at,
            "company_name": company_name,
            "url": url,
        },
    }


# --- Client: trigger n8n workflow ---

class TriggerWorkflowRequest(BaseModel):
    """Body for /api/trigger-workflow. Sent to n8n webhook."""
    query: str
    num_websites: int = 5


@app.post("/api/trigger-workflow")
def trigger_workflow(body: TriggerWorkflowRequest):
    """
    Forward the payload to the n8n webhook. Set N8N_WEBHOOK_URL in the environment
    to your n8n workflow webhook URL (e.g. https://your-n8n.com/webhook/...).
    """
    webhook_url = os.environ.get("N8N_WEBHOOK_URL")
    if not webhook_url or not webhook_url.strip():
        raise HTTPException(
            status_code=503,
            detail="N8N_WEBHOOK_URL is not set. Set it in the environment and restart the server.",
        )
    payload = {
        "query": body.query.strip(),
        "num_websites": max(1, min(100, body.num_websites)),
    }
    try:
        r = httpx.post(webhook_url, json=payload, timeout=30.0)
        r.raise_for_status()
        return {"ok": True, "message": "Workflow triggered"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"n8n webhook returned {e.response.status_code}: {e.response.text[:200]}",
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Could not reach n8n: {e}")


# --- Serve frontend (static) ---

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/")
    def index():
        """Serve the client-side app."""
        index_path = STATIC_DIR / "index.html"
        if not index_path.is_file():
            raise HTTPException(status_code=404, detail="index.html not found")
        return FileResponse(index_path)
