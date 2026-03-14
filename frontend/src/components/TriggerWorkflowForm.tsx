import { useState, FormEvent } from 'react';
import { triggerWorkflow } from '../api';

type Message = { text: string; type: 'error' | 'success' } | null;

export default function TriggerWorkflowForm() {
  const [query, setQuery] = useState('');
  const [numWebsites, setNumWebsites] = useState(5);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<Message>(null);

  const showMessage = (text: string, type: 'error' | 'success') => setMessage({ text, type });
  const clearMessage = () => setMessage(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    clearMessage();
    const q = query.trim();
    if (!q) {
      showMessage('Please enter some text (search or topic).', 'error');
      return;
    }
    if (numWebsites < 1 || numWebsites > 20) {
      showMessage('Please choose between 1 and 20 websites.', 'error');
      return;
    }
    setLoading(true);
    try {
      await triggerWorkflow({ query: q, num_websites: numWebsites });
      showMessage('Workflow triggered successfully.', 'success');
    } catch (err) {
      showMessage(err instanceof Error ? err.message : 'Workflow trigger failed.', 'error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form className="form" onSubmit={handleSubmit} noValidate>
        <div className="field">
          <label htmlFor="query">Search or topic (free text)</label>
          <input
            type="text"
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. local restaurants in Austin, gyms near Denver"
            autoComplete="off"
          />
        </div>
        <div className="field">
          <label htmlFor="num-websites">
            Number of websites to analyze
            <output aria-live="polite"> {numWebsites}</output>
          </label>
          <input
            type="range"
            id="num-websites"
            min={1}
            max={20}
            value={numWebsites}
            step={1}
            onChange={(e) => setNumWebsites(Number(e.target.value))}
          />
        </div>
        <button type="submit" className="btn" disabled={loading}>
          Trigger workflow
        </button>
      </form>
      {message != null && (
        <div className={`message ${message.type}`} role="status" aria-live="polite">
          {message.text}
        </div>
      )}
    </>
  );
}
