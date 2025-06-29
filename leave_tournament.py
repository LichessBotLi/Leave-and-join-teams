#!/usr/bin/env python3
"""
Withdraw from the Lichess arena tournament r7hAA1Hq.

Environment
-----------
LEAVE : str
    Personal-access token with the “tournament:write” scope.

Returns exit-status 0 on success, ≠0 on error.
"""
from __future__ import annotations

import os
import sys
import requests

TOURNAMENT_ID = "r7hAA1Hq"                       # ← the “tmt” you linked
API_URL = f"https://lichess.org/api/tournament/{TOURNAMENT_ID}/withdraw"


def main() -> None:
    token = os.environ.get("LEAVE")
    if not token:
        sys.exit("Environment variable LEAVE is missing.")

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(API_URL, headers=headers, timeout=15)

    if r.status_code == 200:                      # success per API spec 0
        print("✅  Successfully withdrew from the tournament.")
    elif r.status_code == 401:
        sys.exit("❌  Invalid or expired token.")
    elif r.status_code == 404:
        sys.exit("❌  Tournament not found, or you were not registered.")
    else:
        sys.exit(f"❌  HTTP {r.status_code}: {r.text}")


if __name__ == "__main__":
    main()
