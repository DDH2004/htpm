#!/bin/sh

echo ":: Skipping the worktree will prevent files in this directory from being"
echo ":: accidentally commited to the git repository. Paths are relative."

git update-index --skip-worktree vpn/*/*.ovpn
git update-index --skip-worktree wap/*
git update-index --skip-worktree scorebot/*
git update-index --skip-worktree ../challenges/0_Smart-Home/_firmware/wap/config.ino
git update-index --skip-worktree ../challenges/2_Power-Grid/_firmware/wap/config.ino
