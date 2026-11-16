# Reproduction and artifact integrity

Run the README commands from the project root. The core and native package sets
are separately pinned in requirements-locks. The native lock records the exact
official upstream commit, rather than accepting any package named lightrag.

Generate with --resume to reuse only checksum-matching datasets. An index key
includes the corpus hash, split, condition, full architecture settings, native
version/commit/Python, and implementation source hash. Generation jobs include
the exact prompt and dataset manifest hashes. Any mismatch rejects reuse.

Every writer uses an exclusive .job.lock and atomic replacement. A killed
process can leave a stale lock: inspect its PID and logs before removing only
that lock. Dataset/index directories that contain incomplete artifacts are
rejected; use a fresh directory. Per-case generation jobs can resume completed,
checksum-matching cases. Failed native attempts remain in numbered trace folders.
The code never silently overwrites a completed/frozen snapshot.

The bundled pilot and evidence can be inspected without calling any models.
Native fixture reproduction requires installed dependencies and verified
tokenizer assets, but no inference credentials. Real provider runs require
credentials; no secrets are embedded in the package. `.env.example` is a template,
not an automatically loaded credentials file.

Expected meaningful checks: core pytest suite, opt-in native SDK integration,
Ruff, dataset audit, all 48 native pilot queries, strict output validation and
idempotent resume. The implementation report records actual outcomes. Test
fixtures and deterministic test-model outputs are not scientific measurements.

