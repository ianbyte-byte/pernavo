# Evidence methods

## USE and RED

For every resource, record utilization, saturation and errors. For a user-facing service, also record traffic, errors and latency. Preserve metric names, units, query, window, dimensions and aggregation.

## Traces and metrics

Use spans to connect endpoint latency to downstream calls, queueing, retries and serialization. Use stable OpenTelemetry semantic conventions and bounded route/service dimensions. Latency should retain a histogram or equivalent percentile evidence; average alone is insufficient.

## Retries

Separate original requests from retry attempts. Record connect/request/deadline timeouts, attempt count, backoff, jitter, retryable errors and per-layer policies. Check for multiplicative retries across call layers.

## Sources

- USE: https://www.brendangregg.com/usemethod.html
- Methodology: https://www.brendangregg.com/methodology.html
- OTel observability primer: https://opentelemetry.io/docs/concepts/observability-primer/
- OTel metrics data model: https://opentelemetry.io/docs/specs/otel/metrics/data-model/
- OTel trace API: https://opentelemetry.io/docs/specs/otel/trace/api/
- Google SRE monitoring: https://sre.google/sre-book/monitoring-distributed-systems/
- AWS retry guidance: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
