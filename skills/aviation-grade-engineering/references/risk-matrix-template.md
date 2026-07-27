# Risk Assessment Matrix

## Risk Classification

| Level | Impact | Examples | Required Rigor |
|-------|--------|----------|----------------|
| **Critical** | Data loss, safety risk, regulatory violation, financial loss | Medical data processing, payment systems, auth/crypto, data consistency | Full traceability, 90%+ test coverage, formal review, SLO monitoring |
| **High** | Significant user impact, data corruption | Report generation, core business logic, API contracts, integrations | 80%+ test coverage, integration tests, CI gates, structured logging |
| **Medium** | Degraded experience, recoverable errors | UI workflows, notifications, non-critical batch jobs | Unit + integration tests, basic monitoring, error handling |
| **Low** | Minimal impact, internal tools | Admin panels, internal dashboards, prototypes | Basic tests, lint, code review |

## Assessment Questions

For each module, answer:

1. **What happens if this fails?** (data loss? user impact? revenue loss?)
2. **Who is affected?** (patients? all users? internal staff?)
3. **Is the failure reversible?** (can we roll back? is data corrupted permanently?)
4. **Are there regulatory requirements?** (HIPAA? PCI-DSS? GDPR?)
5. **How often does this code change?** (stable core vs. frequently changing)

## Scoring

- Answer each question 1-5 (1 = minimal risk, 5 = maximum risk)
- Total score determines risk level:
  - 20-25: Critical
  - 15-19: High
  - 10-14: Medium
  - 5-9: Low
