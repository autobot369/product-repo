#!/usr/bin/env python3
"""
Monthly market-research scheduler.

Fires the market-research agent on a configurable schedule (default: 4th of each month at 09:00 UTC).
Schedule is controlled by tools/config.yml → pm_workers.scheduler.
Output is appended to scheduler.log.

Usage:
  python scheduler.py              # start scheduler (blocking)
  python scheduler.py --run-now    # fire immediately and exit (for testing)

Run as background service (survives terminal close):
  nohup python scheduler.py > scheduler.log 2>&1 &

To stop:
  kill $(cat scheduler.pid)
"""

import argparse
import logging
import os
import time
from datetime import datetime
from pathlib import Path

import pytz

LOG_FILE = Path(__file__).parent / "scheduler.log"
PID_FILE = Path(__file__).parent / "scheduler.pid"

# Defaults — overridden at startup by tools/config.yml pm_workers.scheduler.*
_DEFAULTS = {
    "fire_day":  4,
    "fire_hour": 9,
    "fire_min":  0,
    "timezone":  "UTC",
    "topic":     "Tier 1 competitor and innovation trends monthly scan",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [scheduler] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def _should_fire(now: datetime, fire_day: int, fire_hour: int, fire_min: int) -> bool:
    return now.day == fire_day and now.hour == fire_hour and now.minute == fire_min


def _fire(topic: str):
    log.info("Firing market-research — SCHEDULED MONTHLY SCAN")
    try:
        from agents.config import load_config
        from run import run_agent
        config = load_config()
        run_agent("market-research", {"Topic": topic, "Depth": "full"}, config)
        log.info("Monthly research complete.")
    except Exception as e:
        log.error(f"Research failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Monthly market-research scheduler.")
    parser.add_argument("--run-now", action="store_true", help="Fire immediately and exit")
    args = parser.parse_args()

    # Load scheduler settings from config (tools/config.yml → pm_workers.scheduler)
    from agents.config import load_config
    config    = load_config()
    sched_cfg = config.get("scheduler", {})
    fire_day  = int(sched_cfg.get("fire_day",  _DEFAULTS["fire_day"]))
    fire_hour = int(sched_cfg.get("fire_hour", _DEFAULTS["fire_hour"]))
    fire_min  = int(sched_cfg.get("fire_min",  _DEFAULTS["fire_min"]))
    timezone  = pytz.timezone(sched_cfg.get("timezone", _DEFAULTS["timezone"]))
    topic     = sched_cfg.get("topic", _DEFAULTS["topic"])

    # Write PID file so the process can be stopped cleanly
    PID_FILE.write_text(str(os.getpid()))

    if args.run_now:
        log.info("--run-now flag set — firing immediately.")
        _fire(topic)
        PID_FILE.unlink(missing_ok=True)
        return

    log.info(f"Scheduler started. Will run market-research on the {fire_day}th of each month at {fire_hour:02d}:{fire_min:02d} ({sched_cfg.get('timezone', _DEFAULTS['timezone'])}).")
    fired_this_minute = False

    while True:
        now = datetime.now(timezone)

        if _should_fire(now, fire_day, fire_hour, fire_min):
            if not fired_this_minute:
                _fire(topic)
                fired_this_minute = True
        else:
            fired_this_minute = False

        time.sleep(30)  # check every 30 seconds


if __name__ == "__main__":
    main()
