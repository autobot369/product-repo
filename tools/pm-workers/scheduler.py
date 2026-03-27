#!/usr/bin/env python3
"""
Monthly omni-monitor scheduler.

Fires the omni-monitor agent on the 4th of every month at 09:00 SGT.
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

# Lazy import — only needed at fire time
# from run import run_agent
# from agents.config import load_config

LOG_FILE   = Path(__file__).parent / "scheduler.log"
PID_FILE   = Path(__file__).parent / "scheduler.pid"
TIMEZONE   = pytz.timezone("Asia/Singapore")
FIRE_DAY   = 4       # 4th of each month
FIRE_HOUR  = 9       # 09:00 SGT
FIRE_MIN   = 0

MONTHLY_SCAN_PROMPT = (
    "SCHEDULED MONTHLY SCAN — run a full parallel scan of Tier 1 beauty competitors "
    "and innovation trends. Publish to the monthly report page."
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [scheduler] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def _should_fire(now: datetime) -> bool:
    return now.day == FIRE_DAY and now.hour == FIRE_HOUR and now.minute == FIRE_MIN


def _fire():
    log.info("Firing omni-monitor — SCHEDULED MONTHLY SCAN")
    try:
        from agents.config import load_config
        from run import run_agent
        config = load_config()
        run_agent("omni-monitor", {"Request": MONTHLY_SCAN_PROMPT}, config)
        log.info("Monthly scan complete.")
    except Exception as e:
        log.error(f"Scan failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Monthly omni-monitor scheduler.")
    parser.add_argument("--run-now", action="store_true", help="Fire immediately and exit")
    args = parser.parse_args()

    # Write PID file so the process can be stopped cleanly
    PID_FILE.write_text(str(os.getpid()))

    if args.run_now:
        log.info("--run-now flag set — firing immediately.")
        _fire()
        PID_FILE.unlink(missing_ok=True)
        return

    log.info(f"Scheduler started. Will fire on the {FIRE_DAY}th of each month at {FIRE_HOUR:02d}:{FIRE_MIN:02d} SGT.")
    fired_this_minute = False

    while True:
        now = datetime.now(TIMEZONE)

        if _should_fire(now):
            if not fired_this_minute:
                _fire()
                fired_this_minute = True
        else:
            fired_this_minute = False

        time.sleep(30)  # check every 30 seconds


if __name__ == "__main__":
    main()
