# User Personas
> **Status:** Active | **Last Updated:** 2026-03-27

Master registry of all user persona files. Each persona lives at `.claude/personas/<group>/<slug>.md`. Add a row to the relevant segment table and update Behavioral Patterns and Trigger Phrases whenever a new persona is created.

---

## Segment: Shoppers

| Persona | Role | Goals | Main Friction | Tech Savvy |
| :--- | :--- | :--- | :--- | :---: |
| [**Jordan** — Power Buyer](shoppers/power-buyer.md) | High-frequency online shopper | Reorder fast; never re-enter saved data | No one-tap reorder; saved address failures | 4 |

### Behavioral Patterns

- **Jordan:** Speed-maximiser — evaluates by review count and recency, skips product copy entirely. Treats saved payment/address as table stakes; any re-entry prompt triggers abandonment.

### Trigger Phrases

- *Jordan:* "Can I just reorder the same as last time?"
- *Jordan:* "How many reviews does this have — are they recent?"
- *Jordan:* "Why is it asking for my address again?"
- *Jordan:* "There's a redirect here — I'm out."

---

<!-- Add new segments below using the same structure:

## Segment: [Group Name]

| Persona | Role | Goals | Main Friction | Tech Savvy |
| :--- | :--- | :--- | :--- | :---: |
| [**Name** — Title](group/slug.md) | ... | ... | ... | 1–5 |

### Behavioral Patterns
### Trigger Phrases

-->

---

## How to add a persona

1. Generate with `python tools/agent-persona-skill-builder/builder.py --type persona`
2. Save to `.claude/personas/<group>/<slug>.md`
3. Add a row to the relevant segment table above
4. Add one behavioral pattern bullet and 2–3 trigger phrases to that segment's sections

## See also

- [Persona template](../../tools/agent-persona-skill-builder/templates/persona.md)
- [Example persona](../../tools/agent-persona-skill-builder/examples/example-persona.md)
- [Builder tool](../../tools/agent-persona-skill-builder/README.md)
