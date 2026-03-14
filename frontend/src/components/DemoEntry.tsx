import { useState, FormEvent } from 'react';
import { demoStart } from '../api';

type Message = { text: string; type: 'error' | 'success' } | null;

type Props = {
  onStarted?: () => void;
};

export default function DemoEntry({ onStarted }: Props) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<Message>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const u = url.trim();
    if (!u) {
      setMessage({ text: 'Please enter a website URL.', type: 'error' });
      return;
    }
    setMessage(null);
    setLoading(true);
    try {
      await demoStart(u);
      setMessage({ text: 'Demo started. n8n will run the pipeline; watch the strip below.', type: 'success' });
      onStarted?.();
    } catch (err) {
      setMessage({ text: err instanceof Error ? err.message : 'Failed to start demo.', type: 'error' });
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="section demo-entry" aria-labelledby="demo-entry-heading">
      <h2 id="demo-entry-heading">One-URL demo</h2>
      <p className="section-desc">Enter a business website URL and start the pipeline. n8n will run each step and report back here.</p>
      <form className="form demo-entry__form" onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="demo-url">Website URL</label>
          <input
            type="url"
            id="demo-url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            autoComplete="off"
          />
        </div>
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Starting…' : 'Run demo'}
        </button>
      </form>
      {message != null && (
        <div className={`message ${message.type}`} role="status">
          {message.text}
        </div>
      )}
    </section>
  );
}
