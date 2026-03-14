import type { PipelineState, StepId } from '../api';

const STEPS: { id: StepId; label: string }[] = [
  { id: 'discovery', label: 'Discovery' },
  { id: 'assessment', label: 'Assessment' },
  { id: 'build', label: 'Build' },
  { id: 'deploy', label: 'Deploy' },
  { id: 'email', label: 'Email' },
];

type Props = { state: PipelineState | null };

export default function PipelineStrip({ state }: Props) {
  if (!state) return null;

  const steps = state.steps || {};
  const currentStage = state.stage;

  return (
    <div className="pipeline-strip" role="status" aria-live="polite">
      <div className="pipeline-strip__steps">
        {STEPS.map(({ id, label }, i) => {
          const stepState = steps[id];
          const status = stepState?.status ?? 'pending';
          const isActive = currentStage === id && (status === 'running' || status === 'pending');
          const isDone = status === 'done';
          const isError = status === 'error';
          const errorMsg = stepState?.error ?? null;

          return (
            <div
              key={id}
              className={`pipeline-strip__step pipeline-strip__step--${status} ${isActive ? 'pipeline-strip__step--active' : ''}`}
            >
              <div className="pipeline-strip__step-indicator">
                {isDone && <span className="pipeline-strip__check" aria-hidden>✓</span>}
                {isError && <span className="pipeline-strip__x" aria-hidden>✕</span>}
                {status === 'running' && <span className="pipeline-strip__spinner" aria-hidden />}
                {status === 'pending' && <span className="pipeline-strip__dot" aria-hidden />}
              </div>
              <div className="pipeline-strip__step-label">{label}</div>
              {errorMsg && <div className="pipeline-strip__step-error">{errorMsg}</div>}
              {i < STEPS.length - 1 && <div className="pipeline-strip__connector" />}
            </div>
          );
        })}
      </div>
    </div>
  );
}
