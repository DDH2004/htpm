#!/bin/sh

echo ":: Adding files from this directory back to the worktree."

git update-index --no-skip-worktree vpn/*/*.ovpn
