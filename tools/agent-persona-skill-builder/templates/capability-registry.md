# Capability Registry Template — Annotated

A **capability registry** documents what the *product and team* can do — which services exist, who owns them, what APIs they expose, and what tooling runs them. This is distinct from slash-command skill playbooks (which tell Claude *how* to execute a task).

Use this template to give AI agents and PMs a single reference for service discovery, ownership, and integration points.

---

## Token budget breakdown

| Section | Typical tokens | Notes |
|---------|---------------|-------|
| Frontmatter | ~20 | Fixed |
| Capability matrix | ~80–150 | Scales with team size |
| Tooling stack | ~30–60 | LLM ops, deployment, observability |
| Integration map | ~40–80 | API endpoints + doc links |
| **Total** | **~170–310** | Target range |

---

## Template

```markdown
---
name: "{slug}"                          # matches filename without .md
description: "{≤25-word description}"  # what this registry covers and who owns it
type: capability-registry
domain: "{domain}"                      # e.g. checkout, search, growth, platform
last_updated: "{YYYY-MM-DD}"
---

# {Domain} Capability Registry

**Domain:** {domain label}  |  **Owner team:** {team name}  |  **Updated:** {YYYY-MM-DD}

---

## Capability Matrix

<!--
  One row per discrete capability (not per microservice — per user-facing or integration-facing ability).
  Owner: individual or team who is accountable for incidents and roadmap.
  Backup: who covers when Owner is unavailable.
  Status: live | beta | deprecated | planned
  SLA: uptime/latency commitment, or "internal" if no external contract.
-->

| Capability | Owner | Backup | Status | SLA | Notes |
|-----------|-------|--------|--------|-----|-------|
| {Capability one} | {Name / Team} | {Name} | live | {99.9% / <200ms} | {one-line note} |
| {Capability two} | {Name / Team} | {Name} | beta | internal | {one-line note} |
| {Capability three} | {Name / Team} | {Name} | planned | — | Target: {quarter} |

---

## Tooling Stack

<!--
  Document the runtime infrastructure agents need to know about.
  LLM ops: which models are in use and for what purpose.
  Deployment: how services get to production.
  Observability: where logs, metrics, and alerts live.
-->

| Layer | Tool / Service | Purpose |
|-------|---------------|---------|
| LLM ops | {e.g. Claude Sonnet 4.6} | {e.g. Classification, story generation} |
| Deployment | {e.g. GitHub Actions → ECS} | {e.g. CI/CD for all domain services} |
| Observability | {e.g. Datadog / PagerDuty} | {e.g. Latency dashboards, on-call alerts} |
| Data store | {e.g. Postgres RDS} | {e.g. Primary transactional store} |
| Queue | {e.g. SQS} | {e.g. Async event processing} |

---

## Integration Map

<!--
  API endpoints and documentation links for capabilities that expose an interface.
  Method: HTTP verb or event type.
  Auth: auth mechanism (API key, OAuth, IAM role, none).
  Docs: link to OpenAPI spec, Confluence page, or README.
  Omit internal-only capabilities with no external callers.
-->

| Capability | Endpoint | Method | Auth | Docs |
|-----------|----------|--------|------|------|
| {Capability one} | {/api/v1/path} | GET | API key | {link} |
| {Capability two} | {/api/v1/path} | POST | OAuth 2.0 | {link} |

---

## Usage

<!--
  One-line invocation example. Shows an agent how to reference this registry.
-->
```
Use @.claude/registries/{domain}/{slug}.md — look up owner and API endpoint for {capability}
```

```

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| One row per microservice | One row per user-facing or integration-facing *capability* — services are implementation detail |
| Owner field left as a team name only | Include an individual name — teams don't answer PagerDuty alerts, people do |
| Status not maintained | Add `last_updated` to frontmatter; stale registries mislead agents |
| Integration map lists every internal endpoint | Only list endpoints with external callers — internal wiring belongs in service READMEs |
| Tooling stack too granular | Capture the layer an agent needs to reason about (LLM, deploy, observe) — not every library version |
