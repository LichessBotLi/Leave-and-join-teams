#!/usr/bin/env python3
"""
Join the Lichess team `lichess-swiss` and print the full API response.

Environment variables
---------------------
LEAVE      : personal-access token with the `team:write` scope
TEAM_PASS  : (optional) password if the team is password-protected
TEAM_MSG   : (optional) join message, default "Joined via GitHub Action"
"""

from __future__ import annotations
import os, sys, json, requests, textwrap

TEAM_ID  = "lichess-swiss"                       # ← verified slug
JOIN_URL = f"https://lichess.org/api/team/{TEAM_ID}/join"

def main() -> None:
    token = os.getenv("LEAVE")
    if not token:
        sys.exit("❌  LEAVE environment variable not set.")

    data = {"message": os.getenv("TEAM_MSG", "Joined via GitHub Action")}
    if os.getenv("TEAM_PASS"):
        data["password"] = os.getenv("TEAM_PASS")

    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/json"}      # ask for JSON

    print(f"► POST {JOIN_URL}")
    resp = requests.post(JOIN_URL, headers=headers, data=data, timeout=15)
    print(f"◄ HTTP {resp.status_code}\n{'-'*60}")

    # Show up to 500 chars of the body (pretty-printed JSON if possible)
    try:
        print(json.dumps(resp.json(), indent=2)[:500])
    except Exception:
        print(resp.text[:500])

    print('-'*60)

    if resp.status_code == 200:
        print("✅  Join call succeeded (instant join or request pending).")
    elif resp.status_code == 401:
        sys.exit("❌  Invalid or expired token (401).")
    elif resp.status_code == 404:
        sys.exit(textwrap.dedent(f"""\
❌  Team not found (404).
    • Check the slug (‘{TEAM_ID}’)
    • Ensure your token has `team:write`
    • If you’re already a member, /join returns 404
    • If the team blocks your account type, API returns 404"""))
    else:
        sys.exit(f"❌  HTTP {resp.status_code}: {resp.text[:200]}")

if __name__ == "__main__":
    main()
