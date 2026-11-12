#!/usr/bin/env python3
"""Create isolated repositories; never run an agent or change the real application."""
import argparse
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
for case in sorted((source / "cases").iterdir()):
    target = args.destination / case.name
    shutil.copytree(case, target)
    (target / ".agents").mkdir()
    (target / ".agents/skills").symlink_to(package / "skills", target_is_directory=True)
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
