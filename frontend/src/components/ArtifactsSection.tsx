import type { PipelineState } from '../api';

type Props = { state: PipelineState | null };

export default function ArtifactsSection({ state }: Props) {
  if (!state) return null;

  const { brand_profile, opportunity_report, deployed_url, outreach_email } = state;
  const hasAny = brand_profile || (opportunity_report?.opportunities?.length) || deployed_url || outreach_email;
  if (!hasAny) return null;

  return (
    <section className="section artifacts-section" aria-labelledby="artifacts-heading">
      <h2 id="artifacts-heading">Pipeline artifacts</h2>
      <div className="artifacts-grid">
        {brand_profile && (
          <div className="artifact-card">
            <h3 className="artifact-card__title">Discovery</h3>
            <dl className="artifact-card__dl">
              <dt>Company</dt>
              <dd>{(brand_profile as Record<string, string>).company_name ?? '—'}</dd>
              <dt>Value proposition</dt>
              <dd>{(brand_profile as Record<string, string>).value_proposition ?? '—'}</dd>
              <dt>Colors</dt>
              <dd>
                <span className="artifact-swatch" style={{ background: (brand_profile as Record<string, string>).primary_color }} aria-hidden />
                <span className="artifact-swatch" style={{ background: (brand_profile as Record<string, string>).secondary_color }} aria-hidden />
                {(brand_profile as Record<string, string>).primary_color} / {(brand_profile as Record<string, string>).secondary_color}
              </dd>
            </dl>
          </div>
        )}

        {opportunity_report?.opportunities && opportunity_report.opportunities.length > 0 && (
          <div className="artifact-card">
            <h3 className="artifact-card__title">Assessment</h3>
            <ul className="artifact-list">
              {opportunity_report.opportunities.map((opp, i) => (
                <li key={i}>
                  <strong>{opp.name ?? 'Opportunity'}</strong>
                  {opp.impact && <span className="artifact-list__impact"> ({opp.impact})</span>}
                  {opp.description && <div className="artifact-list__desc">{opp.description}</div>}
                </li>
              ))}
            </ul>
          </div>
        )}

        {deployed_url && (
          <div className="artifact-card">
            <h3 className="artifact-card__title">Deploy</h3>
            <p className="artifact-card__p">
              <a href={deployed_url} target="_blank" rel="noopener noreferrer" className="artifact-link">
                {deployed_url}
              </a>
            </p>
            <p className="artifact-card__hint">Live on Vercel</p>
          </div>
        )}

        {outreach_email && (
          <div className="artifact-card artifact-card--email">
            <h3 className="artifact-card__title">
              <span className="email-sent-badge">Email sent</span>
            </h3>
            <p className="email-meta"><strong>To:</strong> {outreach_email.to ?? '—'}</p>
            <p className="email-meta"><strong>Subject:</strong> {outreach_email.subject ?? '—'}</p>
            {outreach_email.sent_at && (
              <p className="email-meta"><strong>Sent at:</strong> {new Date(outreach_email.sent_at).toLocaleString()}</p>
            )}
            {outreach_email.body && (
              <pre className="email-body">{outreach_email.body}</pre>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
