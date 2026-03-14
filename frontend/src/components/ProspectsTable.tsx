import { useState, useCallback } from 'react';
import { sendOutreach } from '../api';
import type { SentEmail } from '../api';

export type ProspectRow = { id: string; companyName: string; url: string };

const DEMO_ROW: ProspectRow = { id: 'demo', companyName: "Joe's Pizza", url: 'https://example.com' };

export default function ProspectsTable({ onEmailSent }: { onEmailSent: (email: SentEmail) => void }) {
  const [rows, setRows] = useState<ProspectRow[]>([DEMO_ROW]);
  const [newCompany, setNewCompany] = useState('');
  const [newUrl, setNewUrl] = useState('');
  const [message, setMessage] = useState<{ text: string; type: 'error' | 'success' } | null>(null);
  const [sendingId, setSendingId] = useState<string | null>(null);
  const [sentIds, setSentIds] = useState<Set<string>>(new Set());

  const showMessage = useCallback((text: string, type: 'error' | 'success') => {
    setMessage({ text, type });
  }, []);

  const addRow = useCallback(() => {
    const url = newUrl.trim();
    if (!url) {
      showMessage('Please enter a website URL.', 'error');
      return;
    }
    setRows((prev) => [
      ...prev,
      { id: crypto.randomUUID(), companyName: newCompany.trim() || '—', url },
    ]);
    setNewCompany('');
    setNewUrl('');
    setMessage(null);
  }, [newCompany, newUrl, showMessage]);

  const handleSendEmail = useCallback(
    async (row: ProspectRow) => {
      if (sentIds.has(row.id)) return;
      setSendingId(row.id);
      setMessage(null);
      try {
        const res = await sendOutreach({
          url: row.url,
          company_name: row.companyName !== '—' ? row.companyName : undefined,
        });
        setSentIds((prev) => new Set(prev).add(row.id));
        showMessage(`Email sent for ${row.companyName || row.url}.`, 'success');
        onEmailSent(res.email);
      } catch (err) {
        showMessage(err instanceof Error ? err.message : 'Outreach failed.', 'error');
      } finally {
        setSendingId(null);
      }
    },
    [sentIds, onEmailSent, showMessage]
  );

  return (
    <section className="section prospects-section" aria-labelledby="prospects-heading">
      <h2 id="prospects-heading">Prospects</h2>
      <p className="section-desc">Add businesses below and send outreach email per row.</p>

      <div className="add-row form">
        <div className="field field-inline">
          <label htmlFor="new-company-name">Company name</label>
          <input
            type="text"
            id="new-company-name"
            value={newCompany}
            onChange={(e) => setNewCompany(e.target.value)}
            placeholder="e.g. Joe's Pizza"
            autoComplete="off"
          />
        </div>
        <div className="field field-inline">
          <label htmlFor="new-url">Website URL</label>
          <input
            type="url"
            id="new-url"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            placeholder="https://example.com"
            autoComplete="off"
          />
        </div>
        <button type="button" className="btn btn-secondary" onClick={addRow}>
          Add row
        </button>
      </div>

      <div className="table-wrap">
        <table className="prospects-table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Website URL</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => {
              const isSending = sendingId === row.id;
              const isSent = sentIds.has(row.id);
              return (
                <tr key={row.id} className={isSent ? 'row-sent' : ''}>
                  <td className="cell-company">{row.companyName || '—'}</td>
                  <td className="cell-url">
                    <a href={row.url} target="_blank" rel="noopener noreferrer">
                      {row.url}
                    </a>
                  </td>
                  <td className="cell-action">
                    <button
                      type="button"
                      className="btn btn-small send-email-btn"
                      disabled={isSending || isSent}
                      onClick={() => handleSendEmail(row)}
                    >
                      {isSending ? 'Sending…' : isSent ? 'Sent' : 'Send email'}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {message && (
        <div className={`message ${message.type}`} role="status">
          {message.text}
        </div>
      )}
    </section>
  );
}
