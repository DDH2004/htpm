#!/bin/sh

echo ":: Skipping the worktree will prevent files in this directory from being"
echo ":: accidentally commited to the git repository. Paths are relative."

git update-index --skip-worktree vpn/*/*.ovpn
git update-index --skip-worktree wap/*
