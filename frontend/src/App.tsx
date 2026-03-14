import { useState, useCallback } from 'react';
import TriggerWorkflowForm from './components/TriggerWorkflowForm';
import ProspectsTable from './components/ProspectsTable';
import EmailSentSection from './components/EmailSentSection';
import type { SentEmail } from './api';

export default function App() {
  const [lastSentEmail, setLastSentEmail] = useState<SentEmail | null>(null);

  const handleEmailSent = useCallback((email: SentEmail) => {
    setLastSentEmail(email);
  }, []);

  return (
    <main className="container">
      <header className="header">
        <h1>Apex</h1>
        <p className="tagline">Discovery & outreach</p>
      </header>

      <TriggerWorkflowForm />
      <ProspectsTable onEmailSent={handleEmailSent} />
      <EmailSentSection email={lastSentEmail} />
    </main>
  );
}
