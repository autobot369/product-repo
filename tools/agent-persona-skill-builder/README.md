# Agent / Persona / Skill Builder

Interactive CLI that generates token-optimized `.claude/agents/`, `.claude/personas/`, and `.claude/skills/` markdown files for product team use.

---

## Usage

```bash
cd tools/agent-persona-skill-builder

# Interactive mode — prompts for all fields
python builder.py

# Direct mode — specify type upfront
python builder.py --type agent
python builder.py --type persona
python builder.py --type skill

# Write directly to .claude/ instead of printing to stdout
python builder.py --type agent --write
```

No dependencies beyond Python 3.10+ standard library.

---

## What gets generated

| Type | Output location | Purpose |
|------|----------------|---------|
| `agent` | `.claude/agents/<name>.md` | Role persona — shapes how Claude behaves in a session |
| `persona` | `.claude/personas/<group>/<name>.md` | User archetype — reference profile for journey mapping and story design |
| `skill` | `.claude/skills/<name>.md` | Task playbook — defines what Claude executes when a slash command is invoked |

---

## Token Optimization Guidelines

Claude Code reads each file in full every time it is invoked. Every token costs latency and context budget. These rules are enforced by the builder's character limits and templates.

### Agents

| Field | Limit | Why |
|-------|-------|-----|
| `description` (frontmatter) | ≤ 25 words | Used by Claude to decide relevance — be precise, not verbose |
| `identity` | 2–3 sentences | Sets behavioral frame; beyond 3 sentences yields diminishing returns |
| `communication_style` | 1–2 sentences | Tone calibration, not a biography |
| Each `principle` bullet | ≤ 15 words | Bullets compress information density; prose loses it |
| Total principles | 4–7 bullets | More than 7 signals unfocused persona |
| Menu item label | ≤ 10 words | Seen on every session start |

**Activation block:** The standard activation XML block is templated and fixed — do not add commentary or additional steps. It is already optimized for Claude's XML parsing.

**Avoid:**
- Repeating the role in both `role` and `identity`
- Writing principles as multi-sentence explanations
- Adding sub-bullets inside principles
- Annotating menu items with "this command will..."

### Skills

| Field | Limit | Why |
|-------|-------|-----|
| `description` (frontmatter) | ≤ 30 words | This is what appears in Claude's tool-selection reasoning |
| Invocation block | Show only required + optional params | Don't document every edge case |
| Each step | 1 imperative sentence or 1 table | No preamble ("In this step, you will...") |
| Guidelines | Bullets only, ≤ 12 words each | Never prose paragraphs |

**Use tables** for branching logic (template selection, routing rules, report sections) — they carry far more information per token than prose.

**Avoid:**
- Section headers that just restate the step number ("Step 1 — Load Data" → use "## 1 — Load data")
- Restating the persona description in the skill body
- Verbose "Guidelines" sections — 4–6 bullets max

### Personas

| Field | Limit | Why |
|-------|-------|-----|
| `description` (frontmatter) | ≤ 20 words | |
| `identity` | 3–4 sentences | |
| `traits` | 4–6 bullets | |
| `pain_points` | 3–5 bullets | |
| `usage_example` | 1 line | Shows how to invoke in context |

Personas are **reference documents**, not agent files — no activation block, no menu. Keep them readable in under 30 seconds.

---

## Templates

Annotated templates live in `templates/`. They show field placement and include inline comments explaining token tradeoffs:

- [`templates/agent.md`](templates/agent.md)
- [`templates/persona.md`](templates/persona.md)
- [`templates/skill.md`](templates/skill.md)

Examples of fully filled-out output in `examples/`.

---

## Adding to the repo

After generating, commit the file to the appropriate directory:

```bash
# Agent
cp generated-agent.md ../../.claude/agents/<name>.md

# Persona
cp generated-persona.md ../../.claude/personas/<group>/<name>.md

# Skill
cp generated-skill.md ../../.claude/skills/<name>.md
```

Then update `.claude/agents/README.md`, `.claude/skills/README.md`, or `.claude/personas/README.md` to add the new entry to the table.
