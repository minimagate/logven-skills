#!/usr/bin/env python3
"""Create isolated repositories; never run an agent or change the real application."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("destination", type=Path)
args = parser.parse_args()
source = Path(__file__).resolve().parent
package = source.parent
if args.destination.exists():
    parser.error("destination must not exist")
args.destination.mkdir(parents=True)

def fingerprint(directory):
    digest = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(directory)).encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()

snapshot = args.destination / ".skills"
for attempt in range(3):
    before = fingerprint(package / "skills")
    shutil.copytree(package / "skills", snapshot)
    if before == fingerprint(snapshot) == fingerprint(package / "skills"):
        break
    shutil.rmtree(snapshot)
else:
    parser.error("skills kept changing; retry after editing settles")
metadata = {
    "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=package, text=True).strip(),
    "uncommitted_skills": bool(subprocess.check_output(["git", "status", "--porcelain", "--", "skills"], cwd=package)),
    "skills_sha256": before,
}
(args.destination / "PACKAGE.json").write_text(json.dumps(metadata, indent=2) + "\n")
for case in sorted((source / "cases").iterdir()):
    target = args.destination / case.name
    shutil.copytree(case, target)
    (target / ".agents").mkdir()
    (target / ".agents/skills").symlink_to(snapshot.resolve(), target_is_directory=True)
    def git(*command):
        return subprocess.run(["git", *command], cwd=target, check=True, capture_output=True)
    git("init", "-b", "main")
    git("config", "user.name", "Simulation")
    git("config", "user.email", "simulation@example.test")
    git("add", "--all")
    git("commit", "-m", "Simulation baseline")
    if case.name == "refund-review":
        # The endpoint addition is the submitted diff; collaborators predate it.
        git("rm", "--cached", "lib/refund_endpoint.rb", "test/refund_test.rb")
        git("commit", "-m", "Separate proposed endpoint")
        git("add", "-N", "lib/refund_endpoint.rb", "test/refund_test.rb")
    print(target)
