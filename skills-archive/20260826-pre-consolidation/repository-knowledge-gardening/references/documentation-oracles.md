# Documentation Verification Oracles

Choose the narrowest oracle that can establish a claim. Record the command, repository revision,
environment, exit status, artifact, and unverified surfaces. Assessment identifies these checks; it
does not execute commands requiring ungranted authority.

## Deterministic oracles

### Link and path

Check relative links, anchors, referenced files, indexes, and known external URL observations. An
external request result is time- and environment-specific and does not establish semantic currency.

### Structure and metadata

Check required headings, unique identifiers, status values, owners, source declarations, plan state,
cross-links, and separation of active, completed, generated, and historical artifacts.

### Documented commands

Parse and, when authorized, run README, bootstrap, test, release, and runbook commands in the named
environment. Shell syntax or a copied command is not execution evidence. Network, credentials,
writes, migrations, and production access require separate authority.

### Code and configuration references

Check that named modules, files, routes, types, configuration keys, environment variables, and test
targets exist. Existence does not establish that the surrounding explanation is correct.

### Generated artifacts

Run the documented generator from canonical inputs in an isolated authorized environment and check
for an unexpected diff. Require provenance; do not hand-edit generated output as the primary fix.

## Semantic and operational oracles

Use trusted product contracts, accepted architecture decisions, independently derived expectations,
tests with reviewed oracles, authorized runtime observation, incident evidence, or an accountable
human decision. Classify results as:

- `supported`;
- `contradicted`;
- `partially-supported`;
- `unverified`.

Do not let the current implementation serve as both the disputed subject and the sole oracle for
intended behavior.

## Promotion rule

When the same critical documentation failure recurs, propose a deterministic control:

| Repeated failure | Prefer |
|---|---|
| Broken navigation | link/index lint |
| Generated schema drift | generator diff check |
| Invalid command | isolated smoke check |
| Architecture dependency violation | structural test |
| Guessed data shape | schema parsing or typed contract |
| Missing plan state | plan metadata/state check |
| Overstated environment claim | evidence-layer validator |

Promotion requires a stable invariant and must not mechanize unresolved product judgment.
