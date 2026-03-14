import type { SentEmail } from '../api';

type Props = { email: SentEmail | null };

export default function EmailSentSection({ email }: Props) {
  if (!email) return null;

  const sentAt = email.sent_at ? new Date(email.sent_at).toLocaleString() : '—';

  return (
    <section className="section email-sent-section" aria-labelledby="email-sent-heading">
      <h2 id="email-sent-heading">Email sent</h2>
      <div className="email-sent-badge" aria-live="polite">
        Email sent
      </div>
      <div className="email-display">
        <p className="email-meta">
          <strong>To:</strong> {email.to || '—'}
        </p>
        <p className="email-meta">
          <strong>Subject:</strong> {email.subject || '—'}
        </p>
        <p className="email-meta">
          <strong>Sent at:</strong> {sentAt}
        </p>
        <div className="email-body-wrap">
          <strong>Body:</strong>
          <pre className="email-body">{email.body || ''}</pre>
        </div>
      </div>
    </section>
  );
}
