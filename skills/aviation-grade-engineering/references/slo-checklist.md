# SLO Definition Checklist

## Step 1: Identify Critical User Journeys

List the top 3-5 things users MUST be able to do:
- [ ] Journey 1: ___ (e.g., "Generate a medical report")
- [ ] Journey 2: ___ (e.g., "Play a video without buffering")
- [ ] Journey 3: ___ (e.g., "Log in and see dashboard")

## Step 2: Define Metrics for Each Journey

For each journey, define:

| Metric | Target | Measurement Window |
|--------|--------|--------------------|
| Availability | e.g., 99.95% | 30-day rolling |
| Latency (P50) | e.g., < 200ms | 5-minute windows |
| Latency (P99) | e.g., < 2s | 5-minute windows |
| Error rate | e.g., < 0.1% | 5-minute windows |
| Throughput | e.g., > 100 req/s | 5-minute windows |

## Step 3: Set Error Budget

- Error budget = 1 - SLO target (e.g., 99.95% → 0.05% budget = ~22 min/month downtime)
- Define policy:
  - Budget > 50%: Normal deployment pace
  - Budget 10-50%: Slow down, focus on reliability
  - Budget < 10%: Freeze non-critical deployments, incident response mode

## Step 4: Instrument

- [ ] Structured logging for all critical paths
- [ ] Metrics collection (OpenTelemetry / Prometheus / Application Insights)
- [ ] Distributed tracing enabled
- [ ] Dashboard created for each SLO
- [ ] Alerting on SLO burn rate (not just threshold)

## Step 5: Review Cadence

- Weekly: Check error budget status
- Monthly: Review SLO targets — are they too loose? Too strict?
- Quarterly: Add/remove SLOs as the system evolves
