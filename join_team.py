#!/usr/bin/env python3
"""
Join the Lichess team `the-raptors`.

Environment
-----------
TEAM : str
    A personal-access token that has the `team:write` scope.
    ⚠️  Must belong to a *human* account if the team disallows bots.
"""

from __future__ import annotations
import os
import sys
import json
import requests

TEAM_ID = "the-raptors"
URL     = f"https://lichess.org/api/team/{TEAM_ID}/join"
MESSAGE = "Joined via GitHub Action"

def main() -> None:
    token = os.environ.get("TEAM")
    if not token:
        sys.exit("TEAM env-var not set.")

    headers = {
        "Authorization": f"Bearer {token}",
        # Forces JSON so we never get an HTML login page 1
        "Accept": "application/json",
    }
    data = {"message": MESSAGE}

    r = requests.post(URL, headers=headers, data=data, timeout=15)

    if r.status_code == 200:
        try:
            if r.json().get("ok"):
                print("✅  Joined The Raptors successfully.")
            else:
                print("ℹ️  Join request sent – waiting for leader approval.")
        except json.JSONDecodeError:
            print("✅  Joined The Raptors successfully (non-JSON body).")
    elif r.status_code == 401:
        sys.exit("❌  Invalid or expired token.")
    elif r.status_code == 404:
        sys.exit(
            "❌  Team not found.\n"
            "    • Check the slug (‘the-raptors’)\n"
            "    • Make sure your token has `team:write`\n"
            "    • Use a human account token if the team blocks bots"
        )
    else:
        sys.exit(f"❌  HTTP {r.status_code}: {r.text}")

if __name__ == "__main__":
    main()
