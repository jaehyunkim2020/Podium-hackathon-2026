const API = '/api';

export type TriggerWorkflowPayload = { query: string; num_websites: number };
export type OutreachPayload = { url: string; company_name?: string | null };
export type SentEmail = {
  subject: string;
  body: string;
  to: string;
  sent_at: string;
  company_name?: string;
  url?: string;
};

export type StepId = 'discovery' | 'assessment' | 'build' | 'deploy' | 'email';
export type StepStatus = 'pending' | 'running' | 'done' | 'error';

export type StepState = {
  status: StepStatus;
  error: string | null;
  payload: Record<string, unknown> | null;
};

export type PipelineState = {
  stage: string;
  target_url: string | null;
  brand_profile: Record<string, unknown> | null;
  error: string | null;
  run_started_at: string | null;
  steps: Record<StepId, StepState>;
  opportunity_report: { opportunities?: Array<{ name?: string; impact?: string; description?: string }> } | null;
  deployed_url: string | null;
  outreach_email: { to?: string; subject?: string; body?: string; sent_at?: string } | null;
};

export async function getState(): Promise<PipelineState> {
  const res = await fetch(`${API}/state`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || 'Failed to fetch state');
  return data as PipelineState;
}

export async function demoStart(url: string): Promise<{ ok: boolean; target_url: string }> {
  const res = await fetch(`${API}/demo/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url.trim() }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || 'Failed to start demo');
  return data as { ok: boolean; target_url: string };
}

export async function triggerWorkflow(payload: TriggerWorkflowPayload): Promise<{ ok: boolean; message?: string }> {
  const res = await fetch(`${API}/trigger-workflow`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || 'Workflow trigger failed');
  return data as { ok: boolean; message?: string };
}

export async function sendOutreach(payload: OutreachPayload): Promise<{ ok: boolean; sent: boolean; email: SentEmail }> {
  const res = await fetch(`${API}/outreach`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail || 'Outreach failed');
  return data as { ok: boolean; sent: boolean; email: SentEmail };
}
