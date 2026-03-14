import { useState, useEffect, useCallback, useRef } from 'react';
import { getState, type PipelineState } from './api';
import TriggerWorkflowForm from './components/TriggerWorkflowForm';
import ProspectsTable from './components/ProspectsTable';
import EmailSentSection from './components/EmailSentSection';
import DemoEntry from './components/DemoEntry';
import PipelineStrip from './components/PipelineStrip';
import ArtifactsSection from './components/ArtifactsSection';
import type { SentEmail } from './api';

const POLL_INTERVAL_MS = 2500;

export default function App() {
  const [lastSentEmail, setLastSentEmail] = useState<SentEmail | null>(null);
  const [pipelineState, setPipelineState] = useState<PipelineState | null>(null);
  const [polling, setPolling] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const handleEmailSent = useCallback((email: SentEmail) => {
    setLastSentEmail(email);
  }, []);

  const handleDemoStarted = useCallback(() => {
    setPolling(true);
  }, []);

  useEffect(() => {
    if (!polling) return;
    const tick = () => {
      getState()
        .then(setPipelineState)
        .catch(() => {});
    };
    tick();
    pollRef.current = setInterval(tick, POLL_INTERVAL_MS);
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
      pollRef.current = null;
    };
  }, [polling]);

  useEffect(() => {
    getState()
      .then((s) => {
        setPipelineState(s);
        if (s?.run_started_at) setPolling(true);
      })
      .catch(() => {});
  }, []);

  return (
    <main className="container">
      <header className="header">
        <h1>Apex</h1>
        <p className="tagline">Discovery & outreach</p>
      </header>

      <DemoEntry onStarted={handleDemoStarted} />
      <PipelineStrip state={pipelineState} />
      {pipelineState?.error && (
        <div className="message error" role="alert">
          {pipelineState.error}
        </div>
      )}
      <ArtifactsSection state={pipelineState} />

      <section className="section" aria-labelledby="trigger-heading">
        <h2 id="trigger-heading">Trigger workflow (n8n)</h2>
        <TriggerWorkflowForm />
      </section>
      <ProspectsTable onEmailSent={handleEmailSent} />
      <EmailSentSection email={lastSentEmail} />
    </main>
  );
}
