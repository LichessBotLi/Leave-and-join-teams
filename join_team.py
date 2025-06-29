#!/usr/bin/env python3
"""
Join the Lichess team `bot-fide-rating`.

Environment
-----------
LEAVE : str   – personal-access token with the `team:write` scope
                (paste it into the GitHub secret named LEAVE).
"""

from __future__ import annotations
import os
import sys
import requests
import json

TEAM_ID  = "bot-fide-rating"
JOIN_URL = f"https://lichess.org/api/team/{TEAM_ID}/join"
MESSAGE  = "Joined via GitHub Action"

def main() -> None:
    token = os.environ.get("LEAVE")        # ← changed from TEAM ➜ LEAVE
    if not token:
        sys.exit("❌  LEAVE environment variable not set.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    data = {"message": MESSAGE}

    resp = requests.post(JOIN_URL, headers=headers, data=data, timeout=15)

    if resp.status_code == 200:
        try:
            ok = resp.json().get("ok", False)
            if ok:
                print("✅  Successfully joined team ‘bot-fide-rating’.")
            else:
                print("ℹ️  Join request sent – awaiting team approval.")
        except json.JSONDecodeError:
            print("✅  Successfully joined (non-JSON response).")
    elif resp.status_code == 401:
        sys.exit("❌  Invalid or expired token (401).")
    elif resp.status_code == 404:
        sys.exit(
            "❌  Team not found (404).\n"
            "    • Check the slug (‘bot-fide-rating’)\n"
            "    • Ensure your token has `team:write`\n"
            "    • If you’re using a bot token and bots are blocked, use a human token."
        )
    else:
        sys.exit(f"❌  HTTP {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    main()
