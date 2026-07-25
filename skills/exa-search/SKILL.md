---
name: exa-search
description: "Call Exa's Search API via cURL for live web search and known-URL content extraction. Default: type auto + highlights for token-efficient agent retrieval; optional /contents, deep search, and outputSchema synthesis."
when_to_use: "Any request like: search the web for X, find recent news or docs, grounded research with citations, fetch clean content for known URLs, structured web enrichment, use Exa, EXA_API_KEY, or prefer neural web search over a browser."
argument-hint: "[search query or URL]"
---

# exa-search — Exa web search via cURL

## Canonical reference

Source of truth for parameters and response shape:

https://exa.ai/docs/reference/search-api-guide-for-coding-agents

If this skill disagrees with that page, **trust the docs** and report the drift.

Markdown mirror (good for agents):  
https://exa.ai/docs/reference/search-api-guide-for-coding-agents.md

## What this skill does

Drives Exa over HTTPS with **cURL + JSON** (no SDK required):

| Need | Endpoint | Default content mode |
|------|----------|----------------------|
| Find pages + excerpts | `POST /search` | `contents.highlights: true` |
| Extract known URLs | `POST /contents` | top-level `highlights: true` |
| Structured grounded answer | `POST /search` + `outputSchema` | still keep highlights when you want raw results too |

**Default agent pattern:** raw `results` + `highlights` (you rank/synthesize). Add `outputSchema` only when you want Exa to return `output.content` + `output.grounding`.

## Auth

```sh
export EXA_API_KEY="YOUR_API_KEY"   # https://dashboard.exa.ai/api-keys
```

Or `.env`:

```env
EXA_API_KEY=YOUR_API_KEY
```

**Headers (both accepted):**

- `x-api-key: $EXA_API_KEY` (used in examples below)
- `Authorization: Bearer $EXA_API_KEY`

Fail closed if the key is missing (401). Never print the key. Never commit it.

## Quick search (default)

```sh
: "${EXA_API_KEY:?EXA_API_KEY is not set}"

curl -sS -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: ${EXA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "recent product announcements from developer tools companies",
    "type": "auto",
    "numResults": 10,
    "contents": {
      "highlights": true
    }
  }'
```

**Stdout (success):** one JSON object with `requestId`, `results[]` (`title`, `url`, `id`, `highlights`, …), optional `searchType` / `costDollars`.

Keep tokens down: prefer **highlights** over full `text`. Cap results (`numResults` 5–10). Only request `text` when excerpts are not enough:

```json
"contents": {
  "text": { "maxCharacters": 15000, "verbosity": "compact" }
}
```

`verbosity`: `"compact"` | `"standard"` | `"full"` (default `"compact"`). Always set `maxCharacters` when requesting text.

## Search types

| `type` | When | Approx latency |
|--------|------|----------------|
| `auto` | **Default** — balanced | ~1s |
| `fast` | Latency-sensitive | ~450ms |
| `instant` | Chat/voice/autocomplete | ~250ms |
| `deep-lite` | Cheap synthesis | ~4s |
| `deep` | Multi-step research / richer synthesis | 4–15s |
| `deep-reasoning` | Hard multi-step reasoning | 12–40s |

`outputSchema` and `contents.maxAgeHours: 0` add latency on top of any type.

Legacy `neural` in old docs/examples → use `auto` for new code.

## Content modes (`/search` → nest under `contents`)

| Mode | Config | Best for |
|------|--------|----------|
| Highlights | `"highlights": true` | Agent loops, token budget |
| Highlights (tuned) | `"highlights": { "query": "...", "maxCharacters": N }` | Bias excerpts / hard cap |
| Text | `"text": { "maxCharacters": 20000 }` | Deep read / RAG |
| Summary | `"summary": true` or `{ "query": "..." }` | Per-result LLM summary |

Combining modes is allowed; starting with **highlights only** is the right default.

### Freshness (`maxAgeHours`)

Under `contents` on `/search` (or top-level on `/contents`):

| Value | Behavior |
|-------|----------|
| omit | Cache when present; livecrawl as fallback (**recommended**) |
| `24` / `1` | Livecrawl if cache older than N hours |
| `0` | Always livecrawl (slowest, freshest) |
| `-1` | Never livecrawl (cache only) |

## Optional filters

```json
{
  "includeDomains": ["arxiv.org", "github.com", "exa.ai/blog", "*.substack.com"],
  "excludeDomains": ["pinterest.com"],
  "category": "news",
  "startPublishedDate": "2025-01-01",
  "userLocation": "US",
  "moderation": true
}
```

`includeDomains` / `excludeDomains` accept domains, path prefixes, and `*.` subdomain wildcards.

**`category`:** `company` | `people` | `publication` | `news` | `personal site` | `financial report`.  
`company` and `people` **reject** `excludeDomains` and date filters (400).

## Structured synthesis (`outputSchema`)

Use when you want Exa to fill a JSON shape with field-level citations in `output.grounding`. Works on **every** `type`; prefer `deep-lite` / `deep` / `deep-reasoning` for harder multi-source work.

```sh
curl -sS -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: ${EXA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "compare the latest frontier AI model releases",
    "type": "deep",
    "systemPrompt": "Prefer official sources, collapse duplicate reporting, keep claims grounded.",
    "outputSchema": {
      "type": "object",
      "required": ["models"],
      "properties": {
        "models": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "notable_claims"],
            "properties": {
              "name": { "type": "string" },
              "notable_claims": {
                "type": "array",
                "items": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "contents": { "highlights": true }
  }'
```

**Schema rules:** max nesting depth **2**, max total properties **10**. Do **not** put citation/confidence fields in the schema — they arrive in `output.grounding`.  
`systemPrompt` = behavior/source rules; `outputSchema` = shape of `output.content`.

`additionalQueries` only for deep variants (`deep-lite` / `deep` / `deep-reasoning`) when you want forced query angles.

## Known URLs: `/contents`

When you already have URLs (no discovery):

```sh
curl -sS -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: ${EXA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": ["https://example.com/article"],
    "highlights": true
  }'
```

On `/contents`, `highlights` / `text` / `summary` / `maxAgeHours` are **top-level** (not under `contents`).  
JSON/cURL: camelCase (`maxCharacters`). Python SDK: snake_case (`max_characters`) even inside nested dicts.

## Streaming

`"stream": true` on `/search` → SSE (`text/event-stream`), OpenAI-style `chat.completion.chunk` frames. Expect chunks, not one JSON body. Skip unless you need progressive UX.

## Agent workflow

1. Confirm `EXA_API_KEY` is set.
2. Run **auto + highlights** first; read `results[].title`, `url`, `highlights`.
3. If evidence is thin: refine `query`, try `type: "deep"`, or add domain/date filters — not all at once.
4. If you need full page body for 1–3 URLs: `/contents` with `text.maxCharacters`, or `/search` with capped `text`.
5. If you need a fixed JSON payload: add `outputSchema` (+ optional deep type); cite from `output.grounding`.
6. Prefer saving large responses to a file and summarizing for the user when result sets are big.

```sh
# Optional: save full JSON, print a short jq view
curl -sS -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: ${EXA_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d @- <<'EOF' | tee /tmp/exa-search.json | jq '{
    n: (.results|length),
    results: [.results[]? | {title, url, highlights: .highlights[0:2]}]
  }'
{
  "query": "YOUR QUERY HERE",
  "type": "auto",
  "numResults": 8,
  "contents": { "highlights": true }
}
EOF
```

## Errors

| HTTP | Meaning |
|------|---------|
| 400 | Bad params / unsupported filter for `category` |
| 401 | Missing or invalid API key |
| 402 | Payment required |
| 422 | Validation error |
| 429 | Rate limit |
| 500 | Server error |

Body shape is often `{"error":"..."}`. Branch on status code; do not invent success from partial output.

## Top pitfalls (do not do these)

1. **`useAutoprompt`** — deprecated; remove entirely.
2. **`includeUrls` / `excludeUrls`** — do not exist; use `includeDomains` / `excludeDomains`.
3. **Top-level `text` / `highlights` / `summary` on `/search`** — must be inside `contents`. On `/contents` they **are** top-level — do not confuse the two.
4. **`numSentences` / `highlightsPerUrl`** — deprecated; use `highlights: true`.
5. **`tokensNum`** — does not exist; use `contents.text.maxCharacters`.
6. **`livecrawl: "always"`** — deprecated; use `contents.maxAgeHours: 0`.
7. **`excludeDomains` or date filters with `category: "company"|"people"`** — 400.
8. **`text: true` with no cap** — can explode context; always cap with `maxCharacters`.
9. **Putting citations in `outputSchema`** — wrong; use `output.grounding`.
10. **Python SDK camelCase inside dicts** — Python wants snake_case throughout; raw JSON/cURL wants camelCase.

## When results are weak / slow / empty

- **Weak relevance:** `type: "auto"` or `"deep"`; more specific singular phrasing; drop over-tight filters.
- **Too slow:** `fast`/`instant`; fewer `numResults`; omit contents if you only need URLs; avoid `maxAgeHours: 0` unless needed.
- **Empty:** remove domain/date/category filters; simplify query; stay on `auto` (has fallbacks).

## Resources

- Docs: https://exa.ai/docs  
- Dashboard / keys: https://dashboard.exa.ai  
- Status: https://status.exa.ai  
- Related endpoints: `/contents`, `/answer` (prefer `/search` + `outputSchema` for new structured search flows)
