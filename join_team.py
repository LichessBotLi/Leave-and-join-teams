#!/usr/bin/env python3
"""
Join the Lichess team.

Environment
-----------
TEAM : str
    Personal-access token with the “team:write” scope.

Usage
-----
• Called without arguments it sends the default join-message
  “Requested via GitHub Action”.

• Optionally pass a custom message:
      python  "Hi, please add me!"

Exit status is 0 on success, ≠0 on error.
"""
from __future__ import annotations

import os
import sys
import requests
import json

TEAM_ID = "the-raptors"
API_URL = f"https://lichess.org/api/team/{TEAM_ID}/join"


def main() -> None:
    token = os.environ.get("TEAM")
    if not token:
        sys.exit("Environment variable TEAM is missing.")

    message = sys.argv[1] if len(sys.argv) > 1 else "Requested via GitHub Action"
    payload = {"message": message}

    headers = {
        "Authorization": f"Bearer {token}",
        # Force JSON so we don’t get the HTML fallback that confused others 0
        "Accept": "application/json",
    }

    r = requests.post(API_URL, headers=headers, data=payload, timeout=15)

    if r.status_code == 200:
        # 200 ⇒ either joined right away or join-request queued for approval
        try:
            data = r.json()
            if data.get("ok"):
                print("✅  Successfully joined the team.")
            else:
                print("ℹ️  Join request sent and awaiting approval.")
        except json.JSONDecodeError:
            # Some teams return an empty body on success
            print("✅  Join request accepted (non-JSON response).")
    elif r.status_code == 401:
        sys.exit("❌  Invalid or expired token.")
    elif r.status_code == 404:
        sys.exit("❌  Team not found.")
    else:
        sys.exit(f"❌  HTTP {r.status_code}: {r.text}")


if __name__ == "__main__":
    main()
