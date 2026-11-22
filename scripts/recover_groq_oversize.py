"""Reopen the Groq ledger after a captured oversize request and budget reduction."""

import argparse
import json
import time

from graphconflictbench.provider_control import ProviderControl, capture_hash


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--evidence-budget", type=int, required=True)
    args = parser.parse_args()
    if not 0 < args.evidence_budget <= 3072:
        parser.error("recovery requires a reduced evidence budget of at most 3072")
    control = ProviderControl(args.policy)
    if control.policy.base_url != "https://api.groq.com/openai/v1":
        parser.error("recovery is only available for Groq")
    control.verify()
    with control.connect() as db:
        db.execute("BEGIN IMMEDIATE")
        if not db.execute("SELECT frozen FROM meta").fetchone()[0]:
            parser.error("provider ledger is already open")
        latest = db.execute(
            "SELECT id,status,response_hash FROM requests WHERE status!='denied' "
            "ORDER BY rowid DESC LIMIT 1"
        ).fetchone()
        if not latest or latest[1] != "uncertain" or not latest[2]:
            parser.error("the latest dispatched request has no captured error response")
        rid, _, expected = latest
        directory = control.root / "requests" / rid
        if capture_hash(directory, "response") != expected:
            parser.error("response capture changed")
        response = json.loads((directory / "response.json").read_bytes())
        error = json.loads((directory / "response.body").read_bytes()).get("error", {})
        if (response.get("status") != 413 or not response.get("body_complete")
                or error.get("type") != "tokens" or error.get("code") != "rate_limit_exceeded"):
            parser.error("the captured response is not a Groq request-size limit")
        db.execute("CREATE TABLE IF NOT EXISTS oversize_recoveries "
                   "(request_id TEXT PRIMARY KEY, recovered_at REAL NOT NULL, evidence_budget INTEGER NOT NULL)")
        db.execute("INSERT INTO oversize_recoveries VALUES (?,?,?)",
                   (rid, time.time(), args.evidence_budget))
        db.execute("UPDATE meta SET frozen=0")
    print(json.dumps(control.verify(), indent=2))


if __name__ == "__main__":
    main()
