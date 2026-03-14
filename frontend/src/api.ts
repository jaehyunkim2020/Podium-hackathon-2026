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
