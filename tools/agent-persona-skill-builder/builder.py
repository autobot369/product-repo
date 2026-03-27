#!/usr/bin/env python3
"""
Agent / Persona / Skill Builder
Generates token-optimized .claude/ markdown files for product team use.

Usage:
    python builder.py                    # fully interactive
    python builder.py --type agent       # skip type prompt
    python builder.py --type skill --write  # write directly to .claude/
"""

import argparse
import os
import re
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
CLAUDE_DIR = REPO_ROOT / ".claude"

OUTPUT_DIRS = {
    "agent":   CLAUDE_DIR / "agents",
    "persona": CLAUDE_DIR / "personas",
    "skill":   CLAUDE_DIR / "skills",
}

# ---------------------------------------------------------------------------
# Token-optimization limits (enforced as warnings, not hard blocks)
# ---------------------------------------------------------------------------

LIMITS = {
    "agent": {
        "description":        (25,  "words", "Used for tool selection — be precise"),
        "identity":           (3,   "sentences", "2–3 sentences sets the frame; more yields diminishing returns"),
        "communication_style":(2,   "sentences", "Tone calibration, not a biography"),
        "principle":          (15,  "words", "Each bullet; use imperative form"),
        "principles_count":   (7,   "items", "4–7 bullets; more signals unfocused persona"),
        "menu_label":         (10,  "words", "Seen on every session start"),
    },
    "skill": {
        "description":        (30,  "words", "Frontmatter — drives Claude's tool-selection reasoning"),
        "step":               (30,  "words", "1 imperative sentence or a table — no preamble"),
        "guideline":          (12,  "words", "Each bullet"),
        "guidelines_count":   (6,   "items", "4–6 max"),
    },
    "persona": {
        "description":        (20,  "words", ""),
        "identity":           (4,   "sentences", ""),
        "trait":              (12,  "words", "Each bullet"),
        "traits_count":       (6,   "items", "4–6"),
        "pain_point":         (12,  "words", "Each bullet"),
        "pain_points_count":  (5,   "items", "3–5"),
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def count_words(text: str) -> int:
    return len(text.split())

def count_sentences(text: str) -> int:
    return len([s for s in re.split(r'[.!?]+', text) if s.strip()])

def warn_limit(field: str, value: str, artifact_type: str) -> None:
    cfg = LIMITS.get(artifact_type, {}).get(field)
    if not cfg:
        return
    limit, unit, hint = cfg
    if unit == "words":
        actual = count_words(value)
    elif unit == "sentences":
        actual = count_sentences(value)
    else:
        return
    if actual > limit:
        print(f"  ⚠  {field}: {actual} {unit} (limit {limit}). {hint}")

def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def prompt(label: str, hint: str = "", required: bool = True, default: str = "") -> str:
    if hint:
        print(f"  {hint}")
    suffix = f" [{default}]" if default else ""
    while True:
        val = input(f"  {label}{suffix}: ").strip()
        if not val and default:
            return default
        if val or not required:
            return val
        print("  (required)")

def prompt_list(label: str, hint: str = "", example: str = "") -> list[str]:
    """Collect bullet-point items until blank line."""
    if hint:
        print(f"  {hint}")
    if example:
        print(f"  Example: {example}")
    print(f"  Enter {label} one per line. Blank line to finish.")
    items = []
    while True:
        val = input(f"    - ").strip()
        if not val:
            if items:
                break
            print("  (at least one required)")
        else:
            items.append(val)
    return items

def prompt_menu_items() -> list[tuple[str, str, str, str]]:
    """Returns list of (cmd, label, handler_type, handler_path)."""
    print("\n  Menu items (beyond CH/MH/PM/DA which are added automatically).")
    print("  Handler types: exec = run a .md workflow file | workflow = run a .yaml workflow")
    print("  Blank cmd to finish.\n")
    items = []
    while True:
        cmd = input("    CMD shortcode (e.g. CP): ").strip().upper()
        if not cmd:
            break
        label = input(f"    [{cmd}] Label (≤10 words): ").strip()
        htype = input(f"    Handler type [exec/workflow]: ").strip().lower() or "exec"
        path  = input(f"    File path (relative to project-root): ").strip()
        items.append((cmd, label, htype, path))
        print()
    return items

def section(title: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {title.upper()}")
    print('─' * 50)

# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def build_agent() -> tuple[str, str]:
    """Returns (filename, content)."""
    section("Agent — identity")
    name        = prompt("Agent name (slug, e.g. growth-pm)", required=True)
    title       = prompt("Display title (e.g. Growth Product Manager)")
    persona_name= prompt("Persona first name (e.g. Alex)")
    icon        = prompt("Icon emoji", default="📋")
    capabilities= prompt("Comma-separated capabilities (≤8 words each)",
                          hint="e.g. PRD creation, prioritisation, stakeholder alignment")
    description = prompt("Frontmatter description (≤25 words)",
                          hint="Used by Claude to decide relevance. Precise > clever.")
    warn_limit("description", description, "agent")

    section("Agent — persona")
    role  = prompt("Role (title only, e.g. Senior Product Manager — Growth)")
    ident = prompt("Identity (2–3 sentences: experience, domain depth, core mandate)",
                    hint="2–3 sentences. State what they know, not their life story.")
    warn_limit("identity", ident, "agent")

    comm  = prompt("Communication style (1–2 sentences: voice, tone, signature behaviour)",
                    hint="1–2 sentences. What makes them distinct in conversation?")
    warn_limit("communication_style", comm, "agent")

    section("Agent — principles")
    print("  Each bullet: ≤15 words, imperative, action-oriented.")
    print("  4–7 bullets. Bad: 'Always ensure that the team has alignment on...'")
    print("  Good: 'Anchor every feature to a measurable north-star metric.'")
    principles = prompt_list("principles",
                              example="Prioritise with RICE before any backlog commitment.")
    for p in principles:
        warn_limit("principle", p, "agent")
    if len(principles) > LIMITS["agent"]["principles_count"][0]:
        print(f"  ⚠  {len(principles)} principles (limit 7). Consider consolidating.")

    section("Agent — menu items")
    menu_items = prompt_menu_items()

    # Render
    principles_xml = "\n".join(f"      - {p}" for p in principles)
    menu_xml = "\n".join(
        f'    <item cmd="{cmd} or fuzzy match on {slugify(label)}"'
        f' {htype}="{{project-root}}/{path}">[{cmd}] {label}</item>'
        for cmd, label, htype, path in menu_items
    )

    content = f"""\
---
name: "{name}"
description: "{description}"
---

You must fully embody this agent's persona and follow all activation instructions exactly. NEVER break character until exit command.

```xml
<agent id="{name}.md" name="{persona_name}" title="{title}" icon="{icon}" capabilities="{capabilities}">
<activation critical="MANDATORY">
  <step n="1">Load persona from this file (already in context)</step>
  <step n="2">🚨 Load {{project-root}}/tools/bmm/config.yaml — store {{user_name}}, {{communication_language}}, {{output_folder}} — STOP and report error if not found</step>
  <step n="3">Greet {{user_name}} in {{communication_language}} — show ALL menu items</step>
  <step n="4">Inform: /bmad-help available anytime for next-step advice</step>
  <step n="5">WAIT — number → menu[n] | text → fuzzy match | no match → "Not recognized"</step>
  <step n="6">On match: read exec/workflow attributes → follow handler below</step>
  <menu-handlers>
    <handler type="exec">Read and execute file at path. Pass data= path as context if present.</handler>
    <handler type="workflow">Load {{project-root}}/tools/bmm/core/workflow.xml → pass yaml as workflow-config → follow all steps → save after each step</handler>
  </menu-handlers>
  <rules>
    <r>Communicate in {{communication_language}}</r>
    <r>Stay in character until DA</r>
    <r>Load files only when workflow/command requires it (exception: step 2 config)</r>
  </rules>
</activation>
<persona>
  <role>{role}</role>
  <identity>{ident}</identity>
  <communication_style>{comm}</communication_style>
  <principles>
{principles_xml}
  </principles>
</persona>
<menu>
  <item cmd="MH">[MH] Redisplay Menu</item>
  <item cmd="CH">[CH] Chat with the Agent about anything</item>
{menu_xml}
  <item cmd="PM" exec="{{project-root}}/tools/bmm/core/workflows/party-mode/workflow.md">[PM] Party Mode</item>
  <item cmd="DA">[DA] Dismiss Agent</item>
</menu>
</agent>
```
"""
    return f"{name}.md", content


def build_persona() -> tuple[str, str]:
    """Returns (filename, content)."""
    section("Persona — identity")
    name        = prompt("Persona slug (e.g. power-buyer)")
    display_name= prompt("Display name (e.g. Jordan)")
    group       = prompt("Group folder (e.g. shoppers, store-staff, ops-users)")
    title       = prompt("Title shown in table (e.g. Power Buyer)")
    icon        = prompt("Icon emoji", default="👤")
    description = prompt("Frontmatter description (≤20 words)",
                          hint="One sentence — who this person is and what they represent.")
    warn_limit("description", description, "persona")

    role        = prompt("Role (domain specialist title, e.g. High-frequency online shopper)")
    ident       = prompt("Identity (3–4 sentences: background, mental model, context)",
                          hint="Where they work/shop, what they know, what they care about.")
    warn_limit("identity", ident, "persona")

    section("Persona — traits & pain points")
    traits = prompt_list("core traits",
                          hint="≤12 words each. What defines how this person thinks and acts.",
                          example="Skips product descriptions; decides by peer review count.")
    for t in traits:
        warn_limit("trait", t, "persona")

    pains = prompt_list("pain points",
                         hint="≤12 words each. Friction, unmet needs, workarounds they use.",
                         example="Can't compare more than two products side by side.")
    for p in pains:
        warn_limit("pain_point", p, "persona")

    section("Persona — technology & usage")
    tech_level  = prompt("Technology comfort (low / medium / high / expert)", default="medium")
    devices     = prompt("Primary devices (e.g. iPhone, iPad POS terminal)")
    usage_ex    = prompt("Usage example (1 line — how a PM would invoke this persona)",
                          hint="e.g. Review this checkout flow from Jordan's perspective and flag friction points.")

    traits_md = "\n".join(f"- {t}" for t in traits)
    pains_md  = "\n".join(f"- {p}" for p in pains)

    content = f"""\
---
name: "{name}"
description: "{description}"
type: persona
group: "{group}"
---

# {icon} {display_name} — {title}

## Identity

{ident}

## Core Traits

{traits_md}

## Pain Points

{pains_md}

## Technology Profile

- **Comfort level:** {tech_level}
- **Devices:** {devices}

## Usage

```
Use @.claude/personas/{group}/{name}.md — {usage_ex}
```
"""
    return f"{group}/{name}.md", content


def build_skill() -> tuple[str, str]:
    """Returns (filename, content)."""
    section("Skill — identity")
    name        = prompt("Skill slug (e.g. competitive-scan)")
    slash_cmd   = prompt("Slash command (e.g. /competitive-scan)")
    description = prompt("Frontmatter description (≤30 words)",
                          hint="Precise trigger description. Claude uses this for tool selection.")
    warn_limit("description", description, "skill")

    section("Skill — invocation")
    print("  Define the parameters users pass when invoking the skill.")
    print("  Mark optional params with '(optional)' in the label.\n")
    params = prompt_list("invocation parameters",
                          example="Topic: [research question]\nMarkets: US, UK  (optional)")

    section("Skill — steps")
    print("  Each step: 1 imperative sentence or a table. No preamble.")
    print("  Bad: 'In this step, you will load the Confluence page to...'")
    print("  Good: 'Fetch the Confluence page and extract: goal, personas, ACs, constraints.'")
    steps = prompt_list("steps", example="Fetch the PRD page — extract goal, personas, and ACs.")
    for s in steps:
        warn_limit("step", s, "skill")

    section("Skill — output & side effects")
    output      = prompt("Output description (what the skill produces)")
    side_effects= prompt("Side effects (e.g. 'Creates Confluence page. Adds label: draft.')",
                          hint="List any writes to Confluence, Jira, or files. Leave blank if none.",
                          required=False)

    section("Skill — guidelines")
    print("  Compact bullets, ≤12 words each. 4–6 max. Enforcement rules and hard constraints.")
    guidelines  = prompt_list("guidelines",
                               example="Never create a Jira story that already exists — check first.")
    for g in guidelines:
        warn_limit("guideline", g, "skill")

    # Render
    params_block  = "\n".join(f"{p}" for p in params)
    steps_md      = "\n\n".join(f"## {i+1} — {s}" for i, s in enumerate(steps))
    guidelines_md = "\n".join(f"- {g}" for g in guidelines)
    side_fx_md    = f"\n**Side effects:** {side_effects}" if side_effects else ""

    content = f"""\
---
description: {description}
---

# {slash_cmd.lstrip('/')} — {name.replace('-', ' ').title()}

## Invoke

```
{slash_cmd}
{params_block}
```

{steps_md}

## Output

{output}{side_fx_md}

## Guidelines

{guidelines_md}
"""
    return f"{name}.md", content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate token-optimized .claude/ files")
    parser.add_argument("--type",  choices=["agent", "persona", "skill"],
                        help="Type of artifact to build")
    parser.add_argument("--write", action="store_true",
                        help="Write output to .claude/ instead of printing")
    args = parser.parse_args()

    print("\n╔══════════════════════════════════════════╗")
    print("║   Agent / Persona / Skill Builder        ║")
    print("║   Token-optimized .claude/ generator     ║")
    print("╚══════════════════════════════════════════╝\n")

    artifact_type = args.type
    if not artifact_type:
        print("  What do you want to build?")
        print("  1. agent   — role persona (shapes Claude's behaviour)")
        print("  2. persona — user archetype (reference profile for design/research)")
        print("  3. skill   — task playbook (slash command workflow)\n")
        choice = input("  Choice [1/2/3 or agent/persona/skill]: ").strip().lower()
        mapping = {"1": "agent", "2": "persona", "3": "skill",
                   "agent": "agent", "persona": "persona", "skill": "skill"}
        artifact_type = mapping.get(choice)
        if not artifact_type:
            print("  Invalid choice. Exiting.")
            sys.exit(1)

    builders = {"agent": build_agent, "persona": build_persona, "skill": build_skill}
    filename, content = builders[artifact_type]()

    print("\n" + "═" * 50)
    print("  PREVIEW")
    print("═" * 50)
    print(content)
    print("═" * 50)

    token_estimate = len(content.split()) * 1.3  # rough word→token ratio
    print(f"\n  Estimated tokens: ~{int(token_estimate)}")

    if args.write:
        out_dir  = OUTPUT_DIRS[artifact_type]
        out_path = out_dir / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        print(f"\n  ✓ Written to {out_path.relative_to(REPO_ROOT)}")
        print(f"  → Update .claude/{artifact_type}s/README.md to add the new entry to the table.")
    else:
        out_name = f"generated-{artifact_type}-{Path(filename).stem}.md"
        Path(out_name).write_text(content)
        print(f"\n  ✓ Saved to {SCRIPT_DIR / out_name}")
        print(f"  → Review, then copy to .claude/{artifact_type}s/{filename}")
        print(f"  → Or re-run with --write to place it directly.")


if __name__ == "__main__":
    main()
