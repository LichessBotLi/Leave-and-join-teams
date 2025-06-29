#!/usr/bin/env python3
"""
Join the Lichess team `chess-enthusiasts` and print the full API response.

Environment variables
---------------------
LEAVE      : personal-access token (must include `team:write`)
TEAM_PASS  : (optional) password if the team is password-protected
TEAM_MSG   : (optional) join message, default "Joined via GitHub Action"
"""

from __future__ import annotations
import os
import sys
import json
import requests
import textwrap

TEAM_ID  = "chess-enthusiasts"              # ← changed slug
JOIN_URL = f"https://lichess.org/api/team/{TEAM_ID}/join"

def main() -> None:
    token = os.getenv("LEAVE")
    if not token:
        sys.exit("❌  LEAVE environment variable not set.")

    message  = os.getenv("TEAM_MSG", "Joined via GitHub Action")
    password = os.getenv("TEAM_PASS")  # may be None

    data = {"message": message}
    if password:
        data["password"] = password

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    print(f"► POST {JOIN_URL}")
    resp = requests.post(JOIN_URL, headers=headers, data=data, timeout=15)
    print(f"◄ HTTP {resp.status_code}\n{'-'*60}")

    # Show up to 500 chars of the body (pretty-printed JSON if possible)
    try:
        parsed = resp.json()
        print(json.dumps(parsed, indent=2)[:500])
    except (json.JSONDecodeError, ValueError):
        print(resp.text[:500])

    print('-' * 60)

    if resp.status_code == 200:
        print("✅  Join call succeeded (instant join or request pending).")
    elif resp.status_code == 401:
        sys.exit("❌  Invalid or expired token (401).")
    elif resp.status_code == 404:
        sys.exit(textwrap.dedent("""\
            ❌  Team not found (404).
                • Check the slug (‘chess-enthusiasts’)
                • Ensure your token has `team:write`
                • If you’re already a member, /join returns 404
                • If the team blocks your account type, API returns 404"""))
    else:
        sys.exit(f"❌  HTTP {resp.status_code}: {resp.text[:200]}")

if __name__ == "__main__":
    main()
