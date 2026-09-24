"""Run a permission matrix against an API and report every cell that does not match.

Each CSV row is one request. Each actor column holds the expected HTTP status for
that actor. Before every cell the probe calls the reset endpoint, so write
requests do not affect each other. After the matrix it runs a few business-rule
scenarios that a status code alone cannot check.

Usage:
  python3 probe.py [--base-url URL] [--matrix FILE] [--reset-path PATH]

Tokens: actor names are used as bearer tokens, which suits the demo API. For a
real system, set TOKEN_<ACTOR> environment variables (dashes become underscores,
upper case), for example TOKEN_ACME_ADMIN. The "anonymous" actor sends no token.
Exit status is 1 when any check fails.
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request

NON_ACTOR_COLUMNS = {"id", "method", "path", "body", "risk", "notes"}


def call(base, method, path, token=None, body=None):
    data = body.encode() if body else (b"{}" if method == "POST" else None)
    req = urllib.request.Request(base + path, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"null")
        except json.JSONDecodeError:
            return e.code, raw.decode(errors="replace")


def token_for(actor):
    if actor == "anonymous":
        return None
    return os.environ.get("TOKEN_" + actor.replace("-", "_").upper(), actor)


def run_matrix(base, matrix, reset_path):
    failures = []
    total = 0
    with open(matrix, newline="") as f:
        for row in csv.DictReader(f):
            actors = [c for c in row if c not in NON_ACTOR_COLUMNS and row[c]]
            for actor in actors:
                expected = int(row[actor])
                if reset_path:
                    call(base, "POST", reset_path)
                status, _ = call(base, row["method"], row["path"], token_for(actor), row["body"] or None)
                total += 1
                if status != expected:
                    failures.append((row["id"], actor, row["method"], row["path"], expected, status, row["risk"]))
    return total, failures


def scenarios(base, reset_path):
    """Business rules for the demo API. Replace with your own for a real system."""
    results = []

    def check(name, ok, detail):
        results.append((name, ok, detail))

    call(base, "POST", reset_path)
    _, orders = call(base, "GET", "/api/orders", token_for("globex-manager"))
    ids = [o["id"] for o in orders] if isinstance(orders, list) else []
    check("tenant list isolation: globex list excludes acme orders", "A-100" not in ids, f"ids={ids}")

    call(base, "POST", reset_path)
    status, _ = call(base, "POST", "/api/invoices/INV-1/payments", token_for("acme-admin"), '{"amount": 600}')
    _, inv = call(base, "GET", "/api/invoices/INV-1", token_for("acme-admin"))
    outstanding = inv.get("outstanding") if isinstance(inv, dict) else None
    check("overpayment rejected and outstanding never below zero",
          status >= 400 and outstanding is not None and outstanding >= 0,
          f"payment of 600 on a 500 balance returned {status}; outstanding now {outstanding}")

    call(base, "POST", reset_path)
    first, _ = call(base, "POST", "/api/orders/A-100/approve", token_for("acme-manager"))
    second, _ = call(base, "POST", "/api/orders/A-100/approve", token_for("acme-manager"))
    check("repeated approval is refused", first == 200 and second == 409, f"first {first}, second {second}")

    return results


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8099")
    ap.add_argument("--matrix", default=os.path.join(here, "permission-matrix.csv"))
    ap.add_argument("--reset-path", default="/__reset", help="empty string to disable")
    ap.add_argument("--no-scenarios", action="store_true")
    args = ap.parse_args()

    total, failures = run_matrix(args.base_url, args.matrix, args.reset_path)
    print(f"permission matrix: {total - len(failures)}/{total} cells as expected")
    if failures:
        print(f"\n{'row':<20}{'actor':<18}{'request':<42}{'expected':>9}{'actual':>8}  risk")
        for rid, actor, method, path, exp, got, risk in failures:
            print(f"{rid:<20}{actor:<18}{method + ' ' + path:<42}{exp:>9}{got:>8}  {risk}")

    failed_scenarios = 0
    if not args.no_scenarios and args.reset_path:
        print("\nbusiness-rule scenarios")
        for name, ok, detail in scenarios(args.base_url, args.reset_path):
            failed_scenarios += not ok
            print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + ("" if ok else f"  ({detail})"))

    sys.exit(1 if failures or failed_scenarios else 0)


if __name__ == "__main__":
    main()
