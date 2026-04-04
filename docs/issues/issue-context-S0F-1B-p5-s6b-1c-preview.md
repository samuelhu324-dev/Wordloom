## Context

- The issue continues the migration of the tracked retained-summary coexistence started by the previous task, focusing on the write_gate retained-summary state of truth.
- It establishes a new primary path at artifacts/s2b.write-gate.runs.latest.json while keeping the legacy alias artifacts/write_gate_runs.latest.json intact for now.
- The team has identified and categorized high-value lookup surfaces, defining which should migrate immediately and which can retain legacy references temporarily.
- Clear dual-read and fallback strategies have been set up to ensure compatibility between generators and consumers without abrupt disruptions during the migration.
