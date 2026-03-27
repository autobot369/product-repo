#!/usr/bin/env python3
"""
PM Agents CLI runner — invokes any skill programmatically via the Claude API.

Usage:
  python run.py <agent> [--arg key=value ...]

Agents:
  create-prd               Create a PRD in Confluence from a brief
  user-stories             Generate Jira stories from a PRD or Confluence context
  omni-monitor             Run competitive intelligence scan
  market-research          Deep-dive market research report
  confluence-user-stories  Bulk generate stories for undocumented Confluence features

Examples:
  python run.py create-prd \\
      --arg "Initiative=Mobile Checkout Redesign" \\
      --arg "Business Problem=High cart abandonment at payment step (current: 42%, target: 25%)" \\
      --arg "User Problem=Users drop off when asked to re-enter payment details" \\
      --arg "Ideal Solution=One-tap checkout with saved payment methods" \\
      --arg "Metrics=Cart abandonment rate, checkout conversion rate"

  python run.py user-stories \\
      --arg "PRD=https://your-org.atlassian.net/wiki/spaces/TEAM/pages/12345" \\
      --arg "Jira project=SQUAD1" \\
      --arg "Epic=SQUAD1-42" \\
      --arg "Board ID=7"

  python run.py omni-monitor \\
      --arg "Request=run a full parallel scan of Tier 1 competitors"

  python run.py market-research \\
      --arg "Topic=AI personalisation in retail 2026" \\
      --arg "Markets=US,UK,AU" \\
      --arg "Depth=full"

  python run.py confluence-user-stories \\
      --arg "Space=TEAM" \\
      --arg "Jira project=SQUAD1" \\
      --arg "Epic=SQUAD1-100"
"""

import argparse
import sys

import anthropic

from agents.config import load_config, load_skill

AGENT_NAMES = ["create-prd", "user-stories", "omni-monitor", "market-research", "confluence-user-stories"]
MODEL       = "claude-opus-4-6"


def build_prompt(skill_text: str, args: dict[str, str]) -> str:
    """Combine skill instructions with user-supplied arguments."""
    args_block = "\n".join(f"{k}: {v}" for k, v in args.items())
    return f"{skill_text}\n\n---\n\n## Run Parameters\n\n{args_block}"


def run_agent(agent: str, args: dict[str, str], config: dict) -> None:
    skill_text = load_skill(agent)
    prompt     = build_prompt(skill_text, args)

    client = anthropic.Anthropic(api_key=config["anthropic_api_key"])

    print(f"\n[pm-agents] Running '{agent}'...\n{'─' * 60}\n")

    with client.messages.stream(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print(f"\n{'─' * 60}\nDone.\n")


def main():
    parser = argparse.ArgumentParser(
        description="PM Agents CLI — run any skill via Claude API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "agent",
        choices=AGENT_NAMES,
        help="Which agent to run",
    )
    parser.add_argument(
        "--arg",
        action="append",
        metavar="KEY=VALUE",
        default=[],
        help="Input argument in KEY=VALUE format (repeat for multiple)",
    )
    args = parser.parse_args()

    # Parse --arg KEY=VALUE pairs
    agent_args: dict[str, str] = {}
    for item in args.arg:
        if "=" not in item:
            print(f"Error: --arg must be in KEY=VALUE format, got: {item!r}")
            sys.exit(1)
        key, _, value = item.partition("=")
        agent_args[key.strip()] = value.strip()

    config = load_config()
    run_agent(args.agent, agent_args, config)


if __name__ == "__main__":
    main()
