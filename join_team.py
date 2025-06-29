#!/usr/bin/env python3
"""
Join the Lichess team and print the full API response.
Environment variables:
  LEAVE      : personal access token (must include `team:write`)
  TEAM_PASS  : (optional) password if the team is password-protected
  TEAM_MSG   : (optional) join message, default "Joined via GitHub Action"
"""

import os
import sys
import json
import requests
import textwrap

TEAM_ID = "lichess-swiss"  # ✅ Your team slug
JOIN_URL = f"https://lichess.org/api/team/{TEAM_ID}/join"

def main():
    token = os.getenv("LEAVE")
    if not token:
        sys.exit("❌ LEAVE environment variable not set.")

    message = os.getenv("TEAM_MSG", "Joined via GitHub Action")
    password = os.getenv("TEAM_PASS")

    payload = {"message": message}
    if password:
        payload["password"] = password

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",  # ✅ Crucial for sending JSON
    }

    print(f"► POST {JOIN_URL}")
    response = requests.post(JOIN_URL, headers=headers, json=payload, timeout=15)  # ✅ Use json=

    print(f"◄ HTTP {response.status_code}\n{'-'*60}")

    try:
        parsed = response.json()
        print(json.dumps(parsed, indent=2)[:500])
    except Exception:
        print(response.text[:500])

    print("-" * 60)

    if response.status_code == 200:
        print("✅  Join call succeeded.")
    elif response.status_code == 401:
        sys.exit("❌  Invalid or expired token.")
    elif response.status_code == 404:
        sys.exit(textwrap.dedent(f"""\
            ❌  Team not found (404).
                • Slug: {TEAM_ID}
                • Token has team:write
                • You are not a member
                • Team allows open joining
                • You can join manually
            Please ensure the request uses JSON body and correct Content-Type.
        """))
    else:
        sys.exit(f"❌  HTTP {response.status_code}: {response.text[:200]}")

if __name__ == "__main__":
    main()
